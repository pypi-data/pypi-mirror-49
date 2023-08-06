# -*- coding: utf-8 -*-
# Copyright 2016-2017 Yelp
# Copyright 2018 Yelp
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
from mrjob.aws import EC2_INSTANCE_TYPE_TO_COMPUTE_UNITS
from mrjob.aws import EC2_INSTANCE_TYPE_TO_MEMORY

from tests.sandbox import BasicTestCase


class EC2InstanceTypeTestCase(BasicTestCase):

    def test_ec2_instance_dicts_match(self):
        self.assertEqual(
            set(EC2_INSTANCE_TYPE_TO_COMPUTE_UNITS),
            set(EC2_INSTANCE_TYPE_TO_MEMORY))
