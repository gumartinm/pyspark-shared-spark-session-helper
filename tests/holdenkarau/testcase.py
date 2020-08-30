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
#            561dddb0d0894c79cf3613688f808aa0ab21f39f/python/sparktestingbase/testcase.py
#

import unittest


class SparkTestingBaseTestCase(unittest.TestCase):

    """Basic common test case for Spark. Provides a Spark context as sc.
    For non local mode testing you can either override sparkMaster
    or set the enviroment property SPARK_MASTER for non-local mode testing."""

    def assertRDDEquals(self, expected, result):
        return self.compareRDD(expected, result) == []

    def compareRDD(self, expected, result):
        expectedKeyed = expected.map(lambda x: (x, 1))\
                                .reduceByKey(lambda x, y: x + y)
        resultKeyed = result.map(lambda x: (x, 1))\
                            .reduceByKey(lambda x, y: x + y)
        return expectedKeyed.cogroup(resultKeyed)\
                            .map(lambda x: tuple(map(list, x[1])))\
                            .filter(lambda x: x[0] != x[1]).take(1)

    def assertRDDEqualsWithOrder(self, expected, result):
        return self.compareRDDWithOrder(expected, result) == []

    def compareRDDWithOrder(self, expected, result):
        def indexRDD(rdd):
            return rdd.zipWithIndex().map(lambda x: (x[1], x[0]))
        indexExpected = indexRDD(expected)
        indexResult = indexRDD(result)
        return indexExpected.cogroup(indexResult)\
                            .map(lambda x: tuple(map(list, x[1])))\
                            .filter(lambda x: x[0] != x[1]).take(1)
