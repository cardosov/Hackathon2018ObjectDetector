import base64
import json
from lumada.utils.communication_channel_util import CommunicationChannelUtil



class LumadaResources:

    @staticmethod
    def create_routing_key(asset_id, gateway_id, message_type, message_name):
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

    @staticmethod
    def create_mqtt_routing_key(asset_id, gateway_id, message_type, message_name):
        # the state msg routing key format should be gateways/{gatewayId}/assets/{assetId}/state
        # the event msg routing key format should be gateways/{gatewayId}/assets/{assetId}/event/{eventName}
        routing_key = ''

        if (gateway_id is not None):
            routing_key = 'gateways/%s/' % (gateway_id)

        routing_key += 'assets/%s/%s'
        routing_key = routing_key % (asset_id, message_type)

        if (message_name is not None):
            routing_key += '/%s'
            routing_key = routing_key % message_name

        return routing_key

    @staticmethod
    def get_credentials_for_message_queue(credentials):
        CommunicationChannelUtil.add_cred_type_to_username(credentials)
