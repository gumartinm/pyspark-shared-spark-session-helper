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
import pathlib

import mock
from pyspark import SparkConf
from pyspark.sql.types import StringType, StructField, StructType

from src.awesome.job.awesome_job import AwesomeJob
from tests.commons import UPPER_CASE_SCHEMA, create_expected_data_frame
from tests.holdenkarau.sqltestcase import SQLTestCase
from tests.shared_spark_session_helper import SharedSparkSessionHelper


class TestAwesomeJob(SharedSparkSessionHelper):
    """Test class for the AwesomeJob."""

    # Each set of tests may run with its own Spark configuration in an isolated way.
    @classmethod
    def spark_conf(cls) -> SparkConf:
        """Return the Spark configuration for the test."""
        conf = super().spark_conf()
        return conf.set('spark.sql.sources.partitionOverwriteMode', 'dynamic')

    def test_run_awesome_job_with_success(self) -> None:
        """Test the successful execution of the `AwesomeJob`."""
        source_path = f"{pathlib.Path(__file__).parent.resolve()}/fixtures/awesomejob/sourcepath/awesome.json"
        destination_path = f"{self.path}/destinationpath/awesomejob/"
        schema = StructType(
            [
                StructField('name', StringType()),
                StructField('surname', StringType())
            ]
        )
        expected_schema = UPPER_CASE_SCHEMA

        with mock.patch('src.awesome.service.awesome_service.AwesomeService', autospec=True) as service_mock:
            service = service_mock.return_value
            service.rename_columns_to_upper_case.return_value = expected_schema
            AwesomeJob(source_path, destination_path, self.spark_session, service).run()

            result_data_frame = self.spark_session.sql('SELECT * FROM testing.example')
            expected_data_frame = create_expected_data_frame(self.spark_session)

            service.rename_columns_to_upper_case.assert_called_once_with(schema)
            data_frame_suite = SQLTestCase()
            data_frame_suite.assertDataFrameEqual(expected=expected_data_frame, result=result_data_frame, tol=0)

    def test_run_awesome_job_again_with_success(self) -> None:
        """Test the successful execution of the `AwesomeJob` with the second set of data."""
        source_path = f"{pathlib.Path(__file__).parent.resolve()}/fixtures/awesomejob/sourcepath/awesome.json"
        destination_path = f"{self.path}/destinationpath/awesomejob/"
        schema = StructType(
            [
                StructField('name', StringType()),
                StructField('surname', StringType())
            ]
        )
        expected_schema = UPPER_CASE_SCHEMA

        with mock.patch('src.awesome.service.awesome_service.AwesomeService', autospec=True) as service_mock:
            service = service_mock.return_value
            service.rename_columns_to_upper_case.return_value = expected_schema
            AwesomeJob(source_path, destination_path, self.spark_session, service).run()

            result_data_frame = self.spark_session.sql('SELECT * FROM testing.example')
            expected_data_frame = create_expected_data_frame(self.spark_session)

            service.rename_columns_to_upper_case.assert_called_once_with(schema)
            data_frame_suite = SQLTestCase()
            data_frame_suite.assertDataFrameEqual(expected=expected_data_frame, result=result_data_frame, tol=0)
