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
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType

UPPER_CASE_SCHEMA = StructType(
    [
        StructField("NAME", StringType()),
        StructField("SURNAME", StringType())
    ]
)


def create_expected_data_frame(spark_session):
    return spark_session.createDataFrame(
        spark_session.sparkContext.parallelize(
            [
                Row("John", "Doe"),
                Row("Jane", "Doe")
            ]),
        UPPER_CASE_SCHEMA
    )
