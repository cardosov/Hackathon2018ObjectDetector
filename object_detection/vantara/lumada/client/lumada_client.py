from lumada.client.uds_client import UdsClient
from lumada.communication.amqp_communication_channel import AmqpCommunicationChannel
from lumada.communication.http_communication_channel import HttpCommunicationChannel
from lumada.communication.mqtt_communication_channel import MqttCommunicationChannel
from lumada.config.communication_channel_config import CommunicationChannelConfig
from lumada.contract.asset_communication_protocol import AssetCommunicationProtocol
from lumada.utils.validator import Validator


class LumadaClient:

    def __init__(self, lumada_client_config=None):
        self._client_config = Validator.validate_config_provided(lumada_client_config, 'LumadaClientConfig')
        self._communication_channel = self._create_lumada_communication_channel(self._client_config)

    def is_connected(self):
        """
        Returns a boolean indicating whether the client is connected to the Lumada platform.
        :return: whether the client is connected to Lumada.
        """
        return self._communication_channel.is_connected()

    def connect(self):
        """
        Establishes a connection with the Lumada platform by using the provided config.
        :raises: exception if attempting to connect when already connected.
        """
        self._communication_channel.connect()

    def disconnect(self):
        """
        Disconnect from the Lumada platform.
        :raises: exception if attempting to disconnect when not connected.
        """
        self._communication_channel.disconnect()

    def publish(self, message):
        """
        Publish a message to Lumada.
        :param message: the message to publish.
        """
        self._communication_channel.publish(message)

    def create_uds_client(self):
        return UdsClient(self._client_config)

    def _create_lumada_communication_channel(self, client_config):
        """
        Helper to create communication channel from the provided config.
        """
        channel_config = CommunicationChannelConfig(hostname=client_config.get_asset_endpoint().get_hostname(),
                                                    username=client_config.get_credentials().get_entity_id(),
                                                    password=client_config.get_credentials().get_entity_value(),
                                                    trust_certs=client_config.get_asset_endpoint().get_trust_all_certificates(),
                                                    requires_secure=client_config.get_asset_endpoint().get_require_secure())

        if client_config.get_protocol() == AssetCommunicationProtocol.AMQP:
            return AmqpCommunicationChannel(channel_config)
        elif client_config.get_protocol() == AssetCommunicationProtocol.HTTP:
            return HttpCommunicationChannel(channel_config)
        else:
            return MqttCommunicationChannel(channel_config)
