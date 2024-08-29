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
from pyspark.sql.types import ArrayType, StringType, StructField, StructType

from src.awesome.service.awesome_service import AwesomeService


class TestAwesomeService:
    """This class contains unit tests for the AwesomeService class."""

    def test_rename_columns_to_upper_case(self) -> None:
        """Test the rename_columns_to_upper_case method of the AwesomeService class."""
        service = AwesomeService()
        some_shema = StructType(
            [
                StructField(
                    'Level1ColumnA',
                    StructType(
                        [
                            StructField(
                                'Level2ColumnA',
                                StructType(
                                    [StructField('Level3ColumnA', StringType())]
                                )
                            )
                        ]
                    )
                ),
                StructField('Level1ColumnB', ArrayType(StringType()))
            ]
        )

        expected_schema = StructType(
            [
                StructField(
                    'LEVEL1COLUMNA',
                    StructType(
                        [
                            StructField(
                                'LEVEL2COLUMNA',
                                StructType(
                                    [StructField('LEVEL3COLUMNA', StringType())]
                                )
                            )
                        ]
                    )
                ),
                StructField('LEVEL1COLUMNB', ArrayType(StringType()))
            ]
        )

        result_schema = service.rename_columns_to_upper_case(some_shema)

        assert expected_schema == result_schema
