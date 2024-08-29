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
import os
import shutil
import tempfile
import uuid
from pathlib import Path

from pyspark import SparkConf
from pyspark.sql import SparkSession


class SharedSparkSessionHelper:
    """Helper class for managing a shared SparkSession."""

    __warehouse_path: Path = None
    __metastore_path: Path = None
    __temporary_path: Path = None

    spark_session: 'SparkSession' = None
    path: Path = None

    @classmethod
    def spark_conf(cls) -> SparkConf:
        """
        Return the SparkConf object for configuring the SparkSession.

        Returns:
            SparkConf: The SparkConf object.
        """
        shutil.rmtree(path=Path('spark-warehouse'), ignore_errors=True)
        shutil.rmtree(path=Path('metastore_db'), ignore_errors=True)
        random_uuid = str(uuid.uuid4())
        cls.__warehouse_path = Path('spark-warehouse', random_uuid)
        cls.__metastore_path = Path('metastore_db', random_uuid)

        return SparkConf() \
            .set('spark.unsafe.exceptionOnMemoryLeak', 'true') \
            .set('spark.ui.enabled', 'false') \
            .set('hive.stats.jdbc.timeout', '80') \
            .set('spark.sql.session.timeZone', 'UTC') \
            .set('spark.sql.warehouse.dir', str(cls.__warehouse_path.absolute())) \
            .set('javax.jdo.option.ConnectionURL',
                 f'jdbc:derby:;databaseName={cls.__metastore_path.absolute()!s};create=true')

    @classmethod
    def setup_class(cls) -> None:
        """
        Set up the class before running any tests.

        This method is executed once before any test method in the class.
        """
        # Before All
        spark_config_path = f"{Path(__file__).parent.resolve()}/conf"
        os.environ['SPARK_CONF_DIR'] = spark_config_path
        cls.spark_session = SparkSession \
            .builder \
            .master('local[2]') \
            .appName('test-sql-context') \
            .config(conf=cls.spark_conf()) \
            .enableHiveSupport() \
            .getOrCreate()

    def setup_method(self) -> None:
        """
        Set up the test method before running it.

        This method is executed before each test method.
        """
        # Before Each
        self.__temporary_path = tempfile.TemporaryDirectory()
        self.path = Path(self.__temporary_path.name)

    def teardown_method(self) -> None:
        """
        Teardown the test method after running it.

        This method is executed after each test method.
        """
        # After Each
        self.__temporary_path.cleanup()

        jvm_session = self.spark_session._jvm.SparkSession.getActiveSession().get()   # pylint: disable=W0212
        jvm_session.sharedState().cacheManager().clearCache()
        jvm_session.sessionState().catalog().reset()

    @classmethod
    def teardown_class(cls) -> None:
        """
        Teardown the class after running all tests.

        This method is executed once after all test methods in the class.
        """
        # After All
        jvm_session = cls.spark_session._jvm.SparkSession.getActiveSession().get()  # pylint: disable=W0212
        jvm_session.clearActiveSession()
        jvm_session.clearDefaultSession()

        cls.spark_session.stop()

        shutil.rmtree(path=cls.__warehouse_path, ignore_errors=True)
        shutil.rmtree(path=cls.__metastore_path, ignore_errors=True)
