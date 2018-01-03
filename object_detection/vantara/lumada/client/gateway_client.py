from lumada.client.api.gateway_client_base import GatewayClientBase
from lumada.utils.validator import Validator
from lumada.client.lumada_client import LumadaClient
from lumada.client.asset_registration_client import AssetRegistrationClient
from lumada.client.asset_client import AssetClient


class GatewayClient(GatewayClientBase):

    def __init__(self, gateway_client_config):
        self._lumada_client = LumadaClient(Validator.validate_config_provided(gateway_client_config, 'AssetClientConfig'))
        self._gateway_id = gateway_client_config.get_credentials().get_entity_id()
        self._gateway_value = gateway_client_config.get_credentials().get_entity_value()
        self._registration_client = AssetRegistrationClient(gateway_id=self._gateway_id,
                                                            gateway_value=self._gateway_value,
                                                            asset_registration_endpoint=gateway_client_config.get_registration_endpoint())

    def register_asset_behind_gateway(self, asset_name, gateway_id, tags):
        """
        Registers an asset behind a gateway
        :param asset_name: Name of asset to register
        :param gateway_id: ID of the gateway to register the client
        :param tags: tags/params to be encoded on the url
        :return: asset client
        """
        Validator.validate_param(asset_name, 'AssetName')
        Validator.validate_param(gateway_id, 'GatewayId')

        asset_id = self._registration_client.register_asset(asset_name=asset_name, gateway_id=gateway_id, properties=tags)
        asset_client =  AssetClient.from_gateway(asset_id=asset_id, gateway_id=self._gateway_id, client=self._lumada_client)

        return asset_client

    def create_asset_client(self, asset_id):
        """
        Create new asset client that communicates with lumada via the gateway
        :param asset_id: ID of the asset to create
        :return: Asset Client
        """
        Validator.validate_param(asset_id, 'AssetId')
        self._registration_client.verify_asset(asset_id=asset_id)
        asset_client =  AssetClient.from_gateway(asset_id=asset_id, gateway_id=self._gateway_id, client=self._lumada_client)
        return asset_client

    def close(self):
        """
        Disconnects from given communication channel
        """
        self._lumada_client.disconnect()
