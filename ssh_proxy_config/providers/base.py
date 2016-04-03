# -*- coding: utf-8 -*-

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
