# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from stevedore import (
    driver,
    extension,
)


def fetch(provider, *args, **kwargs):
    try:
        mgr = driver.DriverManager(
            namespace='ssh_proxy_config.providers',
            name=provider,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds=kwargs,
        )
        return mgr.driver.hosts()
    except RuntimeError:
        print("Cannot find provider plugin named '{}'. Available plugins:".format(provider, file=sys.stderr))
        mgr = extension.ExtensionManager(
            namespace='ssh_proxy_config.providers',
        )
        extensions = sorted([e.name for e in mgr.extensions])
        for e in extensions:
            print('  {}'.format(e), file=sys.stderr)
        sys.exit(1)
