from lumada.client.api.asset_client_base import AssetClientBase
from lumada.client.lumada_client import LumadaClient
from lumada.contract.lumada_message import LumadaMessage
from lumada.contract.lumada_message_type import LumadaMessageType
from lumada.utils.validator import Validator
from lumada.utils.json_util import JsonUtil


class AssetClient(AssetClientBase):

    def __init__(self, asset_client_config=None):
      self._uds_client = None
      if asset_client_config is not None:
          self._client = LumadaClient(asset_client_config)
          self._asset_id = asset_client_config.get_asset_id()
          self._gateway_id = None

    @classmethod
    def from_gateway(cls, asset_id=None, gateway_id=None, client=None):
        cls._client = Validator.validate_param(client, "lumada_client")
        cls._asset_id = Validator.validate_param(asset_id, "asset_id")
        cls._gateway_id = Validator.validate_param(gateway_id, "gateway_id")
        return cls()

    def __enter__(self):
        return self

    def get_asset_identifier(self):
        return self._asset_id

    def publish_event(self, name=None, obj=None):
        Validator.validate_param(name, 'event_name')
        self._publish_message(obj, name, LumadaMessageType.EVENT.value)

    def publish_state(self, obj=None):
        self._publish_message(obj, None, LumadaMessageType.STATE.value)

    def _publish_message(self, obj, name, message_type):
        Validator.validate_param(obj, 'object (to publish)')

        if not self._client.is_connected():
            self._client.connect()

        payload = JsonUtil.serialize_json(obj)

        message = LumadaMessage(message_type=message_type, message_name=name, asset_id=self._asset_id,
                                gateway_id=self._gateway_id, payload=payload)

        self._client.publish(message)

    def put_file(self, file_name, file_path, metadata = {}):
        self.publish_event("fileUploadStartEvent", '{ "fileName" : "%s" }' % (file_name))
        try:
            response = self._get_uds_client().file_put(self._asset_id, file_name, file_path, metadata)
            self.publish_event("fileUploadComplete", '{ "fileName" : "%s" }' % (file_name))
            return response
        except Exception as err:
            self.publish_event("fileUploadFail", '{ "fileName" : "%s", "error" : "%s" }' % (file_name, err))
            raise err

    def get_file(self, file_name):
        return self._get_uds_client().file_get(self._asset_id, file_name)

    def get_file_metadata(self, file_name):
        return self._get_uds_client().file_metadata_get(self._asset_id, file_name)

    def get_file_list(self, prefix=None, marker=None):
        return self._get_uds_client().file_list(self._asset_id, prefix, marker)

    def _get_uds_client(self):
        if self._uds_client is None:
          self._uds_client = self._client.create_uds_client()
        return self._uds_client

    def __exit__(self, exc_type, exc_value, traceback):
        if self._gateway_id is None:
            self._client.disconnect()
