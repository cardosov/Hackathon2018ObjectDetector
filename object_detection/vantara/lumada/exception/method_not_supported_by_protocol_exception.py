"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""


class MethodNotSupportedByProtocolException(Exception):

    def __init__(self, **kwargs):
        self.protocol = kwargs.get('protocol')
        self.method = kwargs.get('method')

    def __str__(self):
        return 'Protocol {0} does not support method {1}'.format(self.protocol, self.method)

