"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

import abc


class LumadaClientConfigBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_credentials(self):
        """
        :return: Client Credentials
        """

    @abc.abstractmethod
    def get_protocol(self):
        """
        :return: Client communication protocol
        """

    @abc.abstractmethod
    def get_asset_endpoint(self):
        """
        :return: Endpoint of the asset
        """

    @abc.abstractmethod
    def get_payload_format(self):
        """
        :return: Payload format used (e.g. JSON, XML)
        """