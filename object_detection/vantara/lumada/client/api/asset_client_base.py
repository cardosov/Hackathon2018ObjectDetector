"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

import abc


class AssetClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def publish_state(self, obj):
        """
        Publishes the last known state of a device
        :param obj:
        :return:
        """

    @abc.abstractmethod
    def publish_event(self, name, obj):
        """
        Publishes an event for a device
        :param obj: Object to publish for state
        :return:
        """

    @abc.abstractmethod
    def get_asset_identifier(self):
        """
        Returns the asset's identifier
        :return: asset identifier
        """
