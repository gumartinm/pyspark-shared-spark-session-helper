# Author: Gustavo Martin Morcuende

#
# Copyright 2020 Gustavo Martin Morcuende
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from pyspark.sql.types import StringType, StructField, StructType


class AwesomeJob:
    __DATABASE = 'testing'
    __TABLE = 'example'

    def __init__(self, source_path, destination_path, spark_session, awesome_service):
        self.source_path = source_path
        self.destination_path = destination_path
        self.spark_session = spark_session
        self.awesome_service = awesome_service
        self.logger = AwesomeJob.__logger(spark_session)

    def run(self):
        self.logger.info('Running AwesomeJob')

        json_schema = StructType(
            [
                StructField('name', StringType()),
                StructField('surname', StringType())
            ]
        )
        data_frame = self.spark_session.read.schema(json_schema).json(path=self.source_path)
        schema = data_frame.schema

        upper_case_schema = self.awesome_service.rename_columns_to_upper_case(schema)
        upper_case_data_frame = self.spark_session.createDataFrame(data_frame.rdd, upper_case_schema)

        self.spark_session.sql(f'CREATE DATABASE IF NOT EXISTS {AwesomeJob.__DATABASE}')
        self.spark_session.sql(
            f'CREATE TABLE IF NOT EXISTS `{AwesomeJob.__DATABASE}`.`{AwesomeJob.__TABLE}` (`NAME` STRING, `SURNAME` STRING) '
            f'USING PARQUET '
            f'OPTIONS ( '
            f'path \'{self.destination_path}\' '
            f')')
        upper_case_data_frame.write \
            .mode('overwrite') \
            .insertInto(f'{AwesomeJob.__DATABASE}.{AwesomeJob.__TABLE}')

        self.logger.info('End running AwesomeJob')

    @staticmethod
    def __logger(spark_session):
        log4j_logger = spark_session.sparkContext._jvm.org.apache.log4j  # pylint: disable=W0212
        return log4j_logger.LogManager.getLogger(__name__)
