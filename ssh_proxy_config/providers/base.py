# -*- coding: utf-8 -*-

# Copyright 2016 VM Farms Inc.
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

import abc
import collections

import six


Host = collections.namedtuple('Host', ['hostname', 'public_ip', 'private_ip'])


@six.add_metaclass(abc.ABCMeta)
class BaseProvider(object):
    """
    Base provider interface.
    """
    @abc.abstractmethod
    def hosts(self):
        """
        Query the appropriate cloud provider and yield hosts belonging to the
        VPC.

        Yields:
            Host objects
        """
        pass
