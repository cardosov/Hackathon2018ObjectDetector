"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.config.api.lumada_client_config_base import LumadaClientConfigBase
from lumada.contract.asset_communication_protocol import AssetCommunicationProtocol
from lumada.exception.missing_param_exception import MissingParamException
from lumada.utils.validator import Validator


class LumadaClientConfig(LumadaClientConfigBase):

    def __init__(self, credentials=None, protocol=None, payload_format=None, asset_endpoint=None):
        self._credentials = Validator.validate_param(credentials, 'credentials')
        self._payload_format = Validator.validate_param(payload_format, 'payload_format')
        self._asset_endpoint = Validator.validate_param(asset_endpoint, 'asset_endpoint')

        if protocol is None:
           protocol = AssetCommunicationProtocol.MQTT

        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def get_asset_endpoint(self):
        return self._asset_endpoint

    def get_credentials(self):
        return self._credentials

    def get_payload_format(self):
        return self._payload_format
