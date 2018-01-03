"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

import abc


class GatewayClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register_asset_behind_gateway(self, asset_name, gateway_id, tags):
        """
        :param asset_name: name of the asset to register
        :param tags: URL tags/parameters for regitering the client
        :return:
        """

    @abc.abstractmethod
    def create_asset_client(self, asset_id):
        """
        Create new asset client that communicates with lumada via the gateway
        :param asset_id: ID of the asset to create
        :return:
        """
