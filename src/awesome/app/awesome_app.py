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
import argparse

from pyspark.sql import SparkSession

from awesome.job.awesome_job import AwesomeJob
from awesome.service.awesome_service import AwesomeService


def run(parsed_args):
    spark_session = SparkSession \
        .builder \
        .appName('awesome-app') \
        .enableHiveSupport() \
        .getOrCreate()

    awesome_service = AwesomeService()

    AwesomeJob(parsed_args.source, parsed_args.destination, spark_session, awesome_service).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Awesome Spark application')
    parser.add_argument('--source', type=str, required=True, dest='source', help='Source path')
    parser.add_argument('--destination', type=str, required=True, dest='destination', help='Destination path')
    args = parser.parse_args()

    run(args)
