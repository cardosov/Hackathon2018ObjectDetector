"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""

from enum import Enum


class AssetCommunicationProtocol(Enum):
    """
    Supported protocols
    """
    MQTT = 'mqtt'

    AMQP = 'amqp'

    HTTP = 'http'

    HTTPS = 'https'
