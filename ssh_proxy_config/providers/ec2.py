# -*- coding: utf-8 -*-

"""
ssh-proxy-config EC2 provider
"""

import boto3

from ssh_proxy_config import Host

def ec2_instances():
    ec2 = boto3.resource('ec2')
    for c in ec2.instances.all():
        hostname = [tag['Value'] for tag in c.tags if tag['Key'] == 'Name'][0]
        yield Host(hostname, c.public_ip_address, c.private_ip_address)