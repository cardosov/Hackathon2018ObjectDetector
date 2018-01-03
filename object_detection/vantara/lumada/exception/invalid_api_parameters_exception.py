"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""


class InvalidApiParametersException(Exception):

    def __init__(self, **kwargs):
        self.parameters = kwargs.get('parameters')

    def __str__(self):
        return 'Missing API parameters of {0}'.format(self.parameters)

