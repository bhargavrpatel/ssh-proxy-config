# -*- coding: utf-8 -*-

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
    return sorted([e.name for e in mgr.extensions])


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
