"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.config.lumada_client_config import LumadaClientConfig
from lumada.utils.validator import Validator


class GatewayClientConfig(LumadaClientConfig):

    def __init__(self, credentials=None, protocol=None, payload_format=None, asset_endpoint=None, gateway_id=None, registration_endpoint=None):
        LumadaClientConfig.__init__(self, credentials, protocol, payload_format, asset_endpoint)
        self._gateway_id = Validator.validate_param(gateway_id, 'gateway_id')
        self._registration_endpoint = Validator.validate_param(registration_endpoint, 'registration_endpoint')

    def get_credentials(self):
        return self._credentials

    def get_entity_id(self):
        return self._credentials._entity_id

    def get_entity_value(self):
        return self._credentials._entity_gateway

    def get_registration_endpoint(self):
        return self._registration_endpoint
