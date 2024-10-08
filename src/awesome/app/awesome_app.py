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
import sys

from pyspark.sql import SparkSession

from src.awesome.job.awesome_job import AwesomeJob
from src.awesome.service.awesome_service import AwesomeService


def run(parsed_args) -> None:
    """
    Run the Awesome Spark application.

    Args:
        parsed_args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        None
    """
    spark_session = SparkSession \
        .builder \
        .appName('awesome-app') \
        .enableHiveSupport() \
        .getOrCreate()

    awesome_service = AwesomeService()

    AwesomeJob(parsed_args.source, parsed_args.destination, spark_session, awesome_service).run()


def main(args: list[str]) -> None:
    """
    Run the main function of the Awesome Spark application.

    Args:
        args (list[str]): Command-line arguments.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Awesome Spark application')

    parser.add_argument('--source',
                        type=str,
                        required=True,
                        dest='source',
                        help='Source path')
    parser.add_argument('--destination',
                        type=str,
                        required=True,
                        dest='destination',
                        help='Destination path')

    args = parser.parse_args(args)
    run(args)


if __name__ == '__main__':
    main(sys.argv[1:])
