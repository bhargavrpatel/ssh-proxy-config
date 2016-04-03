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

"""
ssh-proxy-config EC2 provider
"""

import boto3

from ssh_proxy_config.providers.base import (
    BaseProvider,
    Host,
)


class EC2Provider(BaseProvider):
    def hosts(self):
        ec2 = boto3.resource('ec2')
        for c in ec2.instances.all():
            hostname = [tag['Value'] for tag in c.tags if tag['Key'] == 'Name'][0]
            yield Host(hostname, c.public_ip_address, c.private_ip_address)
