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
Generate SSH configuration for accessing EC2 hosts inside a VPC.

The generated configuration uses ProxyCommand to establish all connections
through a bastion host. By default, the bastion host is the first host whose
hostname contains 'proxy'.

This script uses boto3, and requires either:

  1. AWS credentials defined in ~/.aws/credentials
  2. AWS_SECRET_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
"""

from __future__ import print_function

import argparse
import collections
import sys

import jinja2
import boto3


__version__ = '0.1.0'


Host = collections.namedtuple('Host', ['hostname', 'public_ip', 'private_ip'])


def render(**kwargs):
    env = jinja2.Environment(loader=jinja2.PackageLoader('ssh_proxy_config', 'templates'))
    tmpl = env.get_template('ssh_config.j2')
    return tmpl.render(**kwargs)


def ec2_instances():
    ec2 = boto3.resource('ec2')
    for c in ec2.instances.all():
        hostname = [tag['Value'] for tag in c.tags if tag['Key'] == 'Name'][0]
        yield Host(hostname, c.public_ip_address, c.private_ip_address)


def is_bastion_host(hostname, bastion=None):
    return hostname == bastion or 'proxy' in hostname


def build_ssh_config(user, bastion):
    config = collections.defaultdict(list)
    config['user'] = user
    for host in ec2_instances():
        if is_bastion_host(host.hostname, bastion) and not config['bastion']:
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
    config = build_ssh_config(args.user, args.bastion)
    print(render(**config))


if __name__ == '__main__':
    sys.exit(main())
