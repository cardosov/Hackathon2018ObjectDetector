import pika
import ssl
from lumada.communication.api.communication_channel_base import CommunicationChannelBase
from lumada.exception.asset_client_exception import AssetClientException
from lumada.utils.lumada_resources import LumadaResources
from lumada.utils.json_util import JsonUtil
from lumada.utils.communication_channel_util import CommunicationChannelUtil


class AmqpCommunicationChannel(CommunicationChannelBase):


    def __init__(self, communication_channel_config=None):
        self._connection = None
        self._channel_config = communication_channel_config

    def publish(self, message):
        routing_key = LumadaResources.create_routing_key(message.get_asset_id(),
                                                message.get_gateway_id(),
                                                message.get_message_type(),
                                                message.get_message_name())

        try:
            self._channel.basic_publish(exchange=self._channel_config.get_exchange(),
                                        routing_key=routing_key, body=message.get_payload())
        except Exception as e:
            raise AssetClientException(message="Failed to publish message to rabbitmq.", cause=e)

    def is_connected(self):
        if (self._connection is None):
            return False

        return self._connection.is_open

    def connect(self):
        if self.is_connected():
            raise AssetClientException(message="Illegal State. Amqp client is already connected.")

        TLS_VERSION = "TLSv1.2"

        communication_channel_config = self._channel_config

        ssl_options = {}
        ssl_options["cert_reqs"] = ssl.CERT_REQUIRED if not communication_channel_config.get_trust_certs() else ssl.CERT_NONE
        #client will choose the highest TLS/SSL version both the client and server support

        credentials = pika.PlainCredentials(username=CommunicationChannelUtil.add_cred_type_to_username(communication_channel_config.get_username()),
                                            password=communication_channel_config.get_password())

        connection_params = pika.ConnectionParameters(host=communication_channel_config.get_hostname(),
                                                      credentials=credentials,
                                                      port=5671 if communication_channel_config.get_requires_secure() else 5672,
                                                      virtual_host='producer',
                                                      ssl=communication_channel_config.get_requires_secure(),
                                                      ssl_options=ssl_options)

        try:
            self._connection = pika.BlockingConnection(connection_params)
            self._channel = self._connection.channel()
        except Exception as e:
            raise AssetClientException(message="Error while connecting rabbitmq using AMQP.", cause=e)

    def disconnect(self):
        if not self.is_connected():
            raise AssetClientException(message="Illegal State. Amqp client is not connected.")

        self._connection.close()
