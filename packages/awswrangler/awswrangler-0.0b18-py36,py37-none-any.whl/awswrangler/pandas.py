from io import BytesIO
import multiprocessing as mp
import logging
from math import floor

import pandas
import pyarrow
from pyarrow import parquet

from awswrangler.exceptions import UnsupportedWriteMode, UnsupportedFileFormat
from awswrangler.utils import calculate_bounders
from awswrangler import s3

LOGGER = logging.getLogger(__name__)

MIN_NUMBER_OF_ROWS_TO_DISTRIBUTE = 1000


def _get_bounders(dataframe, num_partitions):
    num_rows = len(dataframe.index)
    return calculate_bounders(num_items=num_rows, num_groups=num_partitions)


class Pandas:
    def __init__(self, session):
        self._session = session

    @staticmethod
    def _parse_path(path):
        path2 = path.replace("s3://", "")
        parts = path2.partition("/")
        return parts[0], parts[2]

    def read_csv(
            self,
            path,
            header="infer",
            names=None,
            dtype=None,
            sep=",",
            lineterminator="\n",
            quotechar='"',
            quoting=0,
            escapechar=None,
            parse_dates=False,
            infer_datetime_format=False,
            encoding=None,
    ):
        bucket_name, key_path = self._parse_path(path)
        s3_client = self._session.boto3_session.client(
            service_name="s3",
            use_ssl=True,
            config=self._session.botocore_config)
        buff = BytesIO()
        s3_client.download_fileobj(bucket_name, key_path, buff)
        buff.seek(0),
        dataframe = pandas.read_csv(
            buff,
            header=header,
            names=names,
            sep=sep,
            quotechar=quotechar,
            quoting=quoting,
            escapechar=escapechar,
            parse_dates=parse_dates,
            infer_datetime_format=infer_datetime_format,
            lineterminator=lineterminator,
            dtype=dtype,
            encoding=encoding,
        )
        buff.close()
        return dataframe

    def read_sql_athena(self, sql, database, s3_output=None):
        if not s3_output:
            account_id = (self._session.boto3_session.client(
                service_name="sts", config=self._session.botocore_config).
                          get_caller_identity().get("Account"))
            session_region = self._session.boto3_session.region_name
            s3_output = f"s3://aws-athena-query-results-{account_id}-{session_region}/"
            s3_resource = self._session.boto3_session.resource("s3")
            s3_resource.Bucket(s3_output)
        query_execution_id = self._session.athena.run_query(
            sql, database, s3_output)
        query_response = self._session.athena.wait_query(
            query_execution_id=query_execution_id)
        if query_response.get("QueryExecution").get("Status").get(
                "State") == "FAILED":
            reason = (query_response.get("QueryExecution").get("Status").get(
                "StateChangeReason"))
            message_error = f"Query error: {reason}"
            raise Exception(message_error)
        else:
            path = f"{s3_output}{query_execution_id}.csv"
            dataframe = self.read_csv(path=path)
        return dataframe

    def to_csv(
            self,
            dataframe,
            path,
            database=None,
            table=None,
            partition_cols=None,
            preserve_index=True,
            mode="append",
            procs_cpu_bound=None,
            procs_io_bound=None,
    ):
        return self.to_s3(
            dataframe=dataframe,
            path=path,
            file_format="csv",
            database=database,
            table=table,
            partition_cols=partition_cols,
            preserve_index=preserve_index,
            mode=mode,
            procs_cpu_bound=procs_cpu_bound,
            procs_io_bound=procs_io_bound,
        )

    def to_parquet(
            self,
            dataframe,
            path,
            database=None,
            table=None,
            partition_cols=None,
            preserve_index=True,
            mode="append",
            procs_cpu_bound=None,
            procs_io_bound=None,
    ):
        return self.to_s3(
            dataframe=dataframe,
            path=path,
            file_format="parquet",
            database=database,
            table=table,
            partition_cols=partition_cols,
            preserve_index=preserve_index,
            mode=mode,
            procs_cpu_bound=procs_cpu_bound,
            procs_io_bound=procs_io_bound,
        )

    def to_s3(
            self,
            dataframe,
            path,
            file_format,
            database=None,
            table=None,
            partition_cols=None,
            preserve_index=True,
            mode="append",
            procs_cpu_bound=None,
            procs_io_bound=None,
    ):
        if not partition_cols:
            partition_cols = []
        if mode == "overwrite" or (mode == "overwrite_partitions"
                                   and not partition_cols):
            self._session.s3.delete_objects(path=path)
        elif mode not in ["overwrite_partitions", "append"]:
            raise UnsupportedWriteMode(mode)
        objects_paths = self.data_to_s3(
            dataframe=dataframe,
            path=path,
            partition_cols=partition_cols,
            preserve_index=preserve_index,
            file_format=file_format,
            mode=mode,
            procs_cpu_bound=procs_cpu_bound,
            procs_io_bound=procs_io_bound,
        )
        if database:
            self._session.glue.metadata_to_glue(
                dataframe=dataframe,
                path=path,
                objects_paths=objects_paths,
                database=database,
                table=table,
                partition_cols=partition_cols,
                preserve_index=preserve_index,
                file_format=file_format,
                mode=mode,
            )
        return objects_paths

    def data_to_s3(
            self,
            dataframe,
            path,
            file_format,
            partition_cols=None,
            preserve_index=True,
            mode="append",
            procs_cpu_bound=None,
            procs_io_bound=None,
    ):
        if not procs_cpu_bound:
            procs_cpu_bound = self._session.procs_cpu_bound
        if not procs_io_bound:
            procs_io_bound = self._session.procs_io_bound
        LOGGER.debug(f"procs_cpu_bound: {procs_cpu_bound}")
        LOGGER.debug(f"procs_io_bound: {procs_io_bound}")
        if path[-1] == "/":
            path = path[:-1]
        file_format = file_format.lower()
        if file_format not in ["parquet", "csv"]:
            raise UnsupportedFileFormat(file_format)
        objects_paths = []
        if procs_cpu_bound > 1:
            bounders = _get_bounders(dataframe=dataframe,
                                     num_partitions=procs_cpu_bound)
            procs = []
            receive_pipes = []
            for bounder in bounders:
                receive_pipe, send_pipe = mp.Pipe()
                proc = mp.Process(
                    target=self._data_to_s3_dataset_writer_remote,
                    args=(
                        send_pipe,
                        dataframe.iloc[bounder[0]:bounder[1], :],
                        path,
                        partition_cols,
                        preserve_index,
                        self._session.primitives,
                        file_format,
                    ),
                )
                proc.daemon = False
                proc.start()
                procs.append(proc)
                receive_pipes.append(receive_pipe)
            for i in range(len(procs)):
                objects_paths += receive_pipes[i].recv()
                procs[i].join()
                receive_pipes[i].close()
        else:
            objects_paths += self._data_to_s3_dataset_writer(
                dataframe=dataframe,
                path=path,
                partition_cols=partition_cols,
                preserve_index=preserve_index,
                session_primitives=self._session.primitives,
                file_format=file_format,
            )
        if mode == "overwrite_partitions" and partition_cols:
            if procs_io_bound > procs_cpu_bound:
                num_procs = floor(
                    float(procs_io_bound) / float(procs_cpu_bound))
            else:
                num_procs = 1
            LOGGER.debug(
                f"num_procs for delete_not_listed_objects: {num_procs}")
            self._session.s3.delete_not_listed_objects(
                objects_paths=objects_paths, procs_io_bound=num_procs)
        return objects_paths

    @staticmethod
    def _data_to_s3_dataset_writer(dataframe, path, partition_cols,
                                   preserve_index, session_primitives,
                                   file_format):
        objects_paths = []
        if not partition_cols:
            object_path = Pandas._data_to_s3_object_writer(
                dataframe=dataframe,
                path=path,
                preserve_index=preserve_index,
                session_primitives=session_primitives,
                file_format=file_format,
            )
            objects_paths.append(object_path)
        else:
            for keys, subgroup in dataframe.groupby(partition_cols):
                subgroup = subgroup.drop(partition_cols, axis="columns")
                if not isinstance(keys, tuple):
                    keys = (keys, )
                subdir = "/".join([
                    f"{name}={val}" for name, val in zip(partition_cols, keys)
                ])
                prefix = "/".join([path, subdir])
                object_path = Pandas._data_to_s3_object_writer(
                    dataframe=subgroup,
                    path=prefix,
                    preserve_index=preserve_index,
                    session_primitives=session_primitives,
                    file_format=file_format,
                )
                objects_paths.append(object_path)
        return objects_paths

    @staticmethod
    def _data_to_s3_dataset_writer_remote(
            send_pipe,
            dataframe,
            path,
            partition_cols,
            preserve_index,
            session_primitives,
            file_format,
    ):
        send_pipe.send(
            Pandas._data_to_s3_dataset_writer(
                dataframe=dataframe,
                path=path,
                partition_cols=partition_cols,
                preserve_index=preserve_index,
                session_primitives=session_primitives,
                file_format=file_format,
            ))
        send_pipe.close()

    @staticmethod
    def _data_to_s3_object_writer(dataframe, path, preserve_index,
                                  session_primitives, file_format):
        fs = s3.get_fs(session_primitives=session_primitives)
        fs = pyarrow.filesystem._ensure_filesystem(fs)
        s3.mkdir_if_not_exists(fs, path)
        if file_format == "parquet":
            outfile = pyarrow.compat.guid() + ".parquet"
        elif file_format == "csv":
            outfile = pyarrow.compat.guid() + ".csv"
        else:
            raise UnsupportedFileFormat(file_format)
        object_path = "/".join([path, outfile])
        if file_format == "parquet":
            Pandas.write_parquet_dataframe(
                dataframe=dataframe,
                path=object_path,
                preserve_index=preserve_index,
                fs=fs,
            )
        elif file_format == "csv":
            Pandas.write_csv_dataframe(
                dataframe=dataframe,
                path=object_path,
                preserve_index=preserve_index,
                fs=fs,
            )
        return object_path

    @staticmethod
    def write_csv_dataframe(dataframe, path, preserve_index, fs):
        csv_buffer = bytes(
            dataframe.to_csv(None, header=False, index=preserve_index),
            "utf-8")
        with fs.open(path, "wb") as f:
            f.write(csv_buffer)

    @staticmethod
    def write_parquet_dataframe(dataframe, path, preserve_index, fs):
        table = pyarrow.Table.from_pandas(df=dataframe,
                                          preserve_index=preserve_index,
                                          safe=False)
        with fs.open(path, "wb") as f:
            parquet.write_table(table, f, coerce_timestamps="ms")

    def to_redshift(
            self,
            dataframe,
            path,
            connection,
            schema,
            table,
            iam_role,
            preserve_index=False,
            mode="append",
    ):
        self._session.s3.delete_objects(path=path)
        num_slices = self._session.redshift.get_number_of_slices(
            redshift_conn=connection)
        LOGGER.debug(f"Number of slices on Redshift: {num_slices}")
        num_rows = len(dataframe.index)
        LOGGER.info(f"Number of rows: {num_rows}")
        if num_rows < MIN_NUMBER_OF_ROWS_TO_DISTRIBUTE:
            num_partitions = 1
        else:
            num_partitions = num_slices
        LOGGER.debug(f"Number of partitions calculated: {num_partitions}")
        objects_paths = self.to_parquet(
            dataframe=dataframe,
            path=path,
            preserve_index=preserve_index,
            mode="append",
            procs_cpu_bound=num_partitions,
        )
        if path[-1] != "/":
            path += "/"
        manifest_path = f"{path}manifest.json"
        self._session.redshift.write_load_manifest(manifest_path=manifest_path,
                                                   objects_paths=objects_paths)
        self._session.redshift.load_table(
            dataframe=dataframe,
            dataframe_type="pandas",
            manifest_path=manifest_path,
            schema_name=schema,
            table_name=table,
            redshift_conn=connection,
            preserve_index=False,
            num_files=num_partitions,
            iam_role=iam_role,
            mode=mode,
        )
        self._session.s3.delete_objects(path=path)
