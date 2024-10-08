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
from pyspark.sql.types import ArrayType, StructField, StructType


class AwesomeService:
    """This is the AwesomeService class."""

    @classmethod
    def rename_columns_to_upper_case(cls, schema: StructType) -> StructType:
        """
        Rename the columns in the schema to upper case.

        Args:
            schema (StructType): The input schema.

        Returns:
            StructType: The schema with renamed columns.
        """
        return cls.__rename_all_cols(schema, cls.__to_upper_case)

    @staticmethod
    def __rename_all_cols(schema: StructType, rename) -> StructType:

        def recur_rename(recur_schema: StructType) -> list[StructField]:
            return [do_rename(field) for field in recur_schema.fields]

        def do_rename(field: StructField) -> StructField:
            if isinstance(field.dataType, StructType):
                return StructField(rename(field.name), StructType(recur_rename(field.dataType)), field.nullable,
                                   field.metadata)

            if isinstance(field.dataType, ArrayType) and isinstance(field.dataType.elementType, StructType):
                return StructField(
                    rename(field.name),
                    ArrayType(
                        StructType(recur_rename(field.dataType.elementType)),
                        field.nullable
                    ),
                    field.nullable,
                    field.metadata
                )

            return StructField(rename(field.name), field.dataType, field.nullable, field.metadata)

        return StructType(recur_rename(schema))

    @staticmethod
    def __to_upper_case(string: str) -> str:
        return string.upper()
