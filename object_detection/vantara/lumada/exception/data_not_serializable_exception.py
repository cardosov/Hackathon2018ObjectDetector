"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""


class DataNotSerializableException(Exception):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

    def __str__(self):
        return 'Asset client exception {0}'.format(self.message)
