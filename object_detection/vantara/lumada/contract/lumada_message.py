class LumadaMessage:

    def __init__(self, message_type=None, payload=None, asset_id=None, gateway_id=None, message_name=None):
        self._message_type = message_type
        self._payload = payload
        self._asset_id = asset_id
        self._gateway_id = gateway_id
        self._message_name = message_name

    def get_message_type(self):
        """
        Retrieve the type(state or event) of the message to publish.
        :return: the message type of the message.
        """
        return self._message_type

    def get_message_name(self):
        """
        Retrieve the message name if it is an event message.
        :return: the message name.
        """
        return self._message_name

    def get_payload(self):
        """
        Retrieve the message payload.
        :return: the message payload.
        """
        return self._payload

    def get_asset_id(self):
        """
        Retrieve the id of the asset to publish for.
        :return: the asset id.
        """
        return self._asset_id

    def get_gateway_id(self):
        """
        Retrieve the gateway id to publish against.
        :return: the gateway id.
        """
        return self._gateway_id