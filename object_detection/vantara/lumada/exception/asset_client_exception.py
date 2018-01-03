"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

class AssetClientException(Exception):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')
        self.cause = kwargs.get('cause')

    def __str__(self):
        return 'Asset client exception {0}: Exception {1}'.format(self.message, self.cause)

