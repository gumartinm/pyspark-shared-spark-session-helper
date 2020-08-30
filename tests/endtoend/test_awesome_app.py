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
from collections import namedtuple

import pytest
from awesome.app.awesome_app import run

from tests.commons import create_expected_data_frame
from tests.holdenkarau.sqltestcase import SQLTestCase
from tests.shared_spark_session_helper import SharedSparkSessionHelper

FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures',
)


@pytest.mark.datafiles(
    os.path.join(FIXTURES_DIR, 'awesomeapp', 'sourcepath'),
    keep_top_dir=True
)
class TestAwesomeApp(SharedSparkSessionHelper):

    def test_run_awesome_app_with_success(self, datafiles):
        source_path = str(datafiles.listdir()[0])
        destination_path = self.path / 'destinationpath/awesomeapp/'

        ParsedArgs = namedtuple('ParsedArgs', 'source destination')
        parsed_args = ParsedArgs(source_path, destination_path)
        run(parsed_args)

        result_data_frame = self.spark_session.sql('SELECT * FROM testing.example')
        expected_data_frame = create_expected_data_frame(self.spark_session)

        data_frame_suite = SQLTestCase()
        data_frame_suite.assertDataFrameEqual(expected=expected_data_frame, result=result_data_frame, tol=0)
