"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""


class InvalidJsonException(Exception):

    def __init__(self, **kwargs):
        self.parameters = kwargs.get('message')

    def __str__(self):
        return 'Json string {0} is invalid. Payloads must be valid json'.format(self.parameters)

