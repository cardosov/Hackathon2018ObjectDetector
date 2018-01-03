"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.config.lumada_client_config import LumadaClientConfig
from lumada.utils.validator import Validator

class AssetClientConfig(LumadaClientConfig):

    def __init__(self, credentials=None, protocol=None, payload_format=None, asset_endpoint=None, asset_id=None):
        LumadaClientConfig.__init__(self, credentials, protocol, payload_format, asset_endpoint)
        self.__asset_id = Validator.validate_param(asset_id, 'asset_id')

    def get_asset_id(self):
        return self.__asset_id
