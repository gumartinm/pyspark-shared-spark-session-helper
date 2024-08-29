# pylint: skip-file

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Taken from: https://github.com/holdenk/spark-testing-base/blob/
#             a44008db92939498ee963d796cb811534e23bf17/python/sparktestingbase/sqltestcase.py
#

import unittest

from pyspark.sql.dataframe import DataFrame


class SQLTestCase(unittest.TestCase):
    """A test case class for SQL operations."""

    def assertDataFrameEqual(self, expected: DataFrame, result: DataFrame, tol: float = 0) -> None:
        """
        Assert that two DataFrames are equal.

        Args:
            expected (DataFrame): The expected DataFrame.
            result (DataFrame): The actual DataFrame.
            tol (float, optional): The tolerance for comparing floating-point values. Defaults to 0.
        """
        self.assertEqual(expected.schema, result.schema)
        try:
            expectedRDD = expected.rdd.cache()
            resultRDD = result.rdd.cache()
            self.assertEqual(expectedRDD.count(), resultRDD.count())

            def zipWithIndex(rdd):
                """Zip with index (idx, data)."""
                return rdd.zipWithIndex().map(lambda x: (x[1], x[0]))

            def equal(x, y) -> bool:
                if (len(x) != len(y)):
                    return False
                elif (x == y):
                    return True
                else:
                    for idx in range(len(x)):
                        a = x[idx]
                        b = y[idx]
                        if isinstance(a, float):
                            if (abs(a - b) > tol):
                                return False
                        else:
                            if a != b:
                                return False
                return True
            expectedIndexed = zipWithIndex(expectedRDD)
            resultIndexed = zipWithIndex(resultRDD)
            joinedRDD = expectedIndexed.join(resultIndexed)
            unequalRDD = joinedRDD.filter(
                lambda x: not equal(x[1][0], x[1][1]))
            differentRows = unequalRDD.take(10)
            self.assertEqual([], differentRows)
        finally:
            expectedRDD.unpersist()
            resultRDD.unpersist()
