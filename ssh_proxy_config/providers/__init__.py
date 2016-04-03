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

from __future__ import print_function

import sys

from stevedore import (
    driver,
    extension,
)


NAMESPACE = 'ssh_proxy_config.providers'


def list_providers():
    mgr = extension.ExtensionManager(
        namespace=NAMESPACE,
    )
    return sorted(mgr.extensions, key=lambda x: x.name)


def fetch(provider, *args, **kwargs):
    try:
        mgr = driver.DriverManager(
            namespace=NAMESPACE,
            name=provider,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds=kwargs,
        )
        return mgr.driver.hosts()
    except RuntimeError:
        print("Cannot find provider plugin named '{}'. Available plugins:".format(provider, file=sys.stderr))
        for e in list_providers():
            print('  {}'.format(e), file=sys.stderr)
        sys.exit(1)
