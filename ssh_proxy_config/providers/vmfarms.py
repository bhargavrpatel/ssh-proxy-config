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
ssh-proxy-config VM Farms provider
"""

import os

from six.moves.urllib.parse import urljoin
import requests

from ssh_proxy_config.providers.base import (
    BaseProvider,
    Host,
)


class VMFarmsAPIClient(object):

    BASE_URL = 'https://my.vmfarms.com/api/v1/'

    def __init__(self, token, url=None):
        self.token = token
        self.url = url if url else self.BASE_URL

    def request(self, method, endpoint, **kwargs):
        url = urljoin(self.url, endpoint)
        kwargs['headers'] = {
            'Authorization': 'Token {}'.format(self.token),
            'Content-Type': 'application/json',
        }
        req = requests.request(method, url, **kwargs)
        return req

    def get(self, resource, **kwargs):
        page = 1
        has_next = True
        while has_next:
            data = self.get_page(resource, page, **kwargs)
            results = data['results']
            for item in results:
                yield item
            page += 1
            has_next = data.get('next', False)

    def get_page(self, endpoint, page, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = page
        kwargs['params'] = params
        req = self.request('GET', endpoint, **kwargs)
        return req.json()


class VMFarmsProvider(BaseProvider):
    def hosts(self):
        client = VMFarmsAPIClient(os.getenv('VMFARMS_API_TOKEN'))
        servers = client.get('servers')
        for server in servers:
            host = Host(
                server['name'],
                server['public_interfaces'][0],
                server['private_interfaces'][0],
            )
            yield host
