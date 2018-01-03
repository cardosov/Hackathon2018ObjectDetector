import json

from lumada.utils.http_util import HttpUtil
from lumada.utils.json_util import JsonUtil

class AssetRegistrationClient():

    def __init__(self, gateway_id, gateway_value, asset_registration_endpoint):
        self._asset_registration_endpoint = asset_registration_endpoint
        self._gateway_id = gateway_id
        self._gateway_value = gateway_value
        self._http_util = HttpUtil(username=self._gateway_id, password=self._gateway_value)

    def register_asset(self, gateway_id, asset_name, properties=None):
        """
        Register asset
        :param asset_name: name of asset to register
        :param gateway_id: tags to register with the asset
        :return: response from register asset api
        """
        register_endpoint = self._http_util.get_endpoint_url(hostname=self._asset_registration_endpoint.get_hostname(),
                                         path='/v1/asset-management/assets', params=None)

        register_payload = {}
        register_payload['gatewayId'] = gateway_id
        register_payload['name'] = asset_name

        register_payload_json = JsonUtil.serialize_json(register_payload)
        payload = register_payload_json
        if properties is not None:
            payload = json.loads(register_payload_json)
            payload.update(properties)

        response = self._http_util.request_json_response(method='post', url=register_endpoint, payload=payload)

        return response['id']

    def verify_asset(self, asset_id):
        """
        Verify asset returns
        :param asset_id: ID of asset to verify
        :return: response of asset verification
        """
        verify_endpoint = self._http_util.get_endpoint_url(hostname=self._asset_registration_endpoint.get_hostname(),
                                        path='/v1/asset-management/assets/%s' % (asset_id),
                                        params=None)

        response = self._http_util.request_json_response(method='get', url=verify_endpoint)

        return response
