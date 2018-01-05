
from lumada.contract.lumada_endpoint import LumadaEndpoint
from lumada.contract.entity_credentials import EntityCredentials
from lumada.client.asset_client import AssetClient
from lumada.config.asset_client_config import AssetClientConfig
from lumada.contract.lumada_message_payload_format import LumadaMessagePayloadFormat
from lumada.contract.asset_communication_protocol import AssetCommunicationProtocol

from threading import Thread

hostname = '172.20.43.25'
entity_id = '4ebdd60e-ef5e-437f-aae3-b93254037313'
entity_value = 'WeIYm5Wxb44PX00dE0LyF88nttxazIZU'

def worker(objName, dangerousObj, level, imgB64):
    credentials = EntityCredentials(entity_id, entity_value)

    endpoint = LumadaEndpoint(hostname, trust_certs=True, require_secure=True)
    config = AssetClientConfig(credentials=credentials, asset_endpoint=endpoint,
                               protocol=AssetCommunicationProtocol.HTTP,
                               payload_format=LumadaMessagePayloadFormat.JSON,
                               asset_id='4ebdd60e-ef5e-437f-aae3-b93254037313')
    client = AssetClient(config)
    payload = {}
    payload['object'] = objName
    payload['dangerous'] = dangerousObj
    payload['level'] = level
    payload['png'] = imgB64

    client.publish_state(payload)
    print("finished... payload: %s " % payload)

def publish_data(obj):
    for i in range(1):
        t = Thread(target=worker, args=(obj['name'], obj['danger'], obj['level'], obj['png']))
        t.daemon = True
        t.start()
