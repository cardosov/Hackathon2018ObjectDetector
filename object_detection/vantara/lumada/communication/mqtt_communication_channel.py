import paho.mqtt.client as mqtt
import ssl
from time import sleep
from lumada.utils.communication_channel_util import CommunicationChannelUtil
from lumada.communication.api.communication_channel_base import CommunicationChannelBase
from lumada.exception.asset_client_exception import AssetClientException
from lumada.utils.lumada_resources import LumadaResources


class MqttCommunicationChannel(CommunicationChannelBase):

    def __init__(self, communication_channel_config=None):
        self._channel_config = communication_channel_config
        self._connected = False
        self._client = mqtt.Client(client_id=self._channel_config.get_username(), transport="ssl")

        if self._channel_config.get_requires_secure():
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
            self._client.tls_set_context(ssl_context)
            if self._channel_config.get_trust_certs():
                self._client.tls_insecure_set(True)

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._connection_failure_retry_count = 0
        self._MAX_RETRY_COUNT = 5

    def publish(self, message):
        routing_key = LumadaResources.create_mqtt_routing_key(message.get_asset_id(),
                                                message.get_gateway_id(),
                                                message.get_message_type(),
                                                message.get_message_name())
        try:
            self._client.publish(topic=routing_key, payload=(message.get_payload()))
        except Exception as e:
            raise AssetClientException(message="Failed to publish message to rabbitmq.", cause=e)

    def is_connected(self):
        return self._connected

    def connect(self):
        if self.is_connected():
            raise AssetClientException(message="Illegal State. Mqtt client is already connected.")

        communication_channel_config = self._channel_config
        self._client.username_pw_set(username='producer:' + CommunicationChannelUtil.add_cred_type_to_username(self._channel_config.get_username()),
                                     password=self._channel_config.get_password())

        try:
            self._client.loop_start()
            self._client.connect(host=communication_channel_config.get_hostname(), port=8883)

            """
            Wait for client to be connected before continuing:
            mqtt_cs_new = 0
            mqtt_cs_connected = 1
            mqtt_cs_disconnecting = 2
            mqtt_cs_connect_async = 3
            """
            while self._client._state != 1:
                if self._connection_failure_retry_count > self._MAX_RETRY_COUNT:
                    raise Exception
                sleep(.5)
                self._connection_failure_retry_count += 1

            self._connection_failure_retry_count = 0
        except Exception as e:
            raise AssetClientException(message="Error while connecting Lumada using MQTT, exceeded max retries of %s"
                                               % self._MAX_RETRY_COUNT)

    def disconnect(self):
        if not self.is_connected():
            raise AssetClientException(message="Illegal State. MQTT client is not connected.")

        self._client.disconnect()

    def _on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            self._connection_failure_retry_count = 0
            self._connected = True
            return
        else:
            self._connection_failure_retry_count += 1
            self._connected = False

        if (rc == 3 or rc > 5) and self._connection_failure_retry_count < self._MAX_RETRY_COUNT:
            # allow connect retry
            return
        else:
            self._client.loop_stop()

            if rc == 1:
                raise AssetClientException(message="Connection refused - incorrect protocol version",
                                           cause="Return Code: %s" % rc)
            elif rc == 2:
                raise AssetClientException(message="Connection refused - invalid client identifier",
                                           cause="Return Code: %s" % rc)
            elif rc == 3:
                raise AssetClientException(message="Connection refused - Lumada Server unavailable",
                                           cause="Return Code: %s" % rc)
            elif rc == 4:
                raise AssetClientException(message="Connection refused - Bad username or password",
                                           cause="Return Code: %s" % rc)
            elif rc == 5:
                raise AssetClientException(message="Connection refused - Unauthorized",
                                           cause="Return Code: %s" % rc)
            else:
                raise AssetClientException(message="Unknown connection error",
                                           cause="Return Code: %s" % rc)

    def _on_disconnect(self, mqttc, userdata, rc):
        self._connected = False
        if rc == 0:
            self._client.loop_stop()

    def _create_routing_key(self, asset_id, gateway_id, message_type, message_name):
        # the state msg routing key format should be gateways.{gatewayId}.assets.{assetId}.state
        # the event msg routing key format should be gateways.{gatewayId}.assets.{assetId}.event.{eventName}
        routing_key = ''

        if(gateway_id is not None):
            routing_key = 'gateways.%s.' % (gateway_id)

        routing_key += 'assets.%s.%s'
        routing_key = routing_key % (asset_id, message_type)

        if(message_name is not None):
            routing_key += '.%s'
            routing_key = routing_key % message_name

        return routing_key
