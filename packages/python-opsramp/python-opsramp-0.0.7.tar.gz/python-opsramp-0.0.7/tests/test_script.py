#!/usr/bin/env python
#
# (c) Copyright 2019 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import unittest
import base64

from opsramp.base import Helpers
from opsramp.rba import Category


class StaticsTest(unittest.TestCase):
    def test_encode_payload(self):
        testfile = 'README.md'
        with open(testfile, 'rb') as f:
            expected = f.read()
        actual64 = Helpers.b64encode_payload(testfile)
        actual = base64.b64decode(actual64)
        assert actual == expected

    def test_mkAttachment(self):
        tvalues = {
            'name': 'whatever.sh',
            'content': 'random stuff'
        }
        actual = Category.mkAttachment(
            name=tvalues['name'],
            payload=tvalues['content']
        )
        expected = {
            'name': tvalues['name'],
            'file': tvalues['content']
        }
        assert actual == expected

    def test_mkParameter(self):
        tvalues = {
            'name': 'venue',
            'description': 'Where am I today?',
            'type': 'STRING'
        }
        actual = Category.mkParameter(
            name=tvalues['name'],
            description=tvalues['description'],
            datatype=tvalues['type']
        )
        expected = {
            'name': tvalues['name'],
            'description': tvalues['description'],
            'dataType': tvalues['type'],
            'type': 'REQUIRED',
            'defaultValue': None
        }
        assert actual == expected

    def test_mkScript(self):
        p1 = Category.mkParameter(
            name='venue',
            description='Where am I today?',
            datatype='STRING'
        )
        tvalues = {
            'name': 'Hello <venue>',
            'description': 'Stereotypical rock star intro',
            'platforms': ['LINUX'],
            'type': 'COMMAND',
            'payload': 'echo "hello $1"',
            'parameters': [p1]
        }
        actual = Category.mkScript(
            name=tvalues['name'],
            description=tvalues['description'],
            platforms=tvalues['platforms'],
            execution_type=tvalues['type'],
            payload=tvalues['payload'],
            parameters=tvalues['parameters']
        )
        expected = {
            'name': tvalues['name'],
            'description': tvalues['description'],
            'platforms': tvalues['platforms'],
            'executionType': tvalues['type'],
            'command': tvalues['payload'],
            'parameters': tvalues['parameters']
        }
        assert actual == expected
