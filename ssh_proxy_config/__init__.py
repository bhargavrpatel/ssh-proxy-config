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
Generate SSH configuration for accessing hosts inside a VPC.

The generated configuration uses ProxyCommand to establish all connections
through a bastion host. By default, the bastion host is the first host whose
hostname contains 'proxy'.
"""

from __future__ import print_function

import argparse
import collections
import sys

import jinja2

from . import providers

__version__ = '0.1.0'


def render(**kwargs):
    env = jinja2.Environment(loader=jinja2.PackageLoader('ssh_proxy_config', 'templates'))
    tmpl = env.get_template('ssh_config.j2')
    return tmpl.render(**kwargs)


def is_bastion_host(hostname, bastion, config, bastion_host_keyword='proxy'):
    # If the user specified a bastion host, always use it.
    if hostname == bastion:
        return True
    # Determine the bastion host based on the keyword if the user did not
    # explicitly choose a host.
    if not config['bastion']:
        return bastion_host_keyword in hostname
    return False


def build_ssh_config(hosts, user, bastion):
    config = collections.defaultdict(list)
    config['user'] = user
    for host in hosts:
        if is_bastion_host(host.hostname, bastion, config):
            config['bastion'] = host
            continue
        config['hosts'].append(host)
    # Sort by hostname.
    config['hosts'] = sorted(config['hosts'], key=lambda h: h.hostname)
    return config


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-p', '--provider',
        choices=providers.list_providers(),
        help='cloud provider (default: %(default)s)',
        default='vmfarms',
    )
    parser.add_argument(
        '-b', '--bastion',
        metavar='BASTION HOST',
        help='bastion host (default: first hostname matching "proxy")',
    )
    parser.add_argument(
        '-u', '--user',
        default='deploy',
        help='SSH user (default: %(default)s)',
    )
    return parser.parse_args()


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]
    args = parse_args(argv)
    hosts = providers.fetch(args.provider)
    config = build_ssh_config(hosts, args.user, args.bastion)
    print(render(**config))


if __name__ == '__main__':
    sys.exit(main())
