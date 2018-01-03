"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

import abc


class CommunicationChannelBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_connected(self):
        """
        Verifies if we are still connected to Lumada.
        :return:
        """

    @abc.abstractmethod
    def connect(self):
        """
        Connects to Lumada platform.
        :return: Client communication protocol
        """

    @abc.abstractmethod
    def disconnect(self):
        """
        Disconnects from the Lumada platform.
        :return: Endpoint of the asset
        """

    @abc.abstractmethod
    def publish(self, message):
        """
        Publishes a message to the Lumada platform.
        :param message: the message to publish.
        :return:
        """
