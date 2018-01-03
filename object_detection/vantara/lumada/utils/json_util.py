import json
from lumada.exception.invalid_json_exception import InvalidJsonException

class JsonUtil:

    @staticmethod
    def serialize_json(payload):
        #if obj has dict attr, use this
        if hasattr(payload, '__dict__'):
            if payload.__dict__ is not None:
                payload_str = json.dumps(payload.__dict__)
                return payload_str
        elif isinstance(payload, dict):
            payload_str = json.dumps(payload)
            return payload_str
        elif isinstance(payload, str):
            try:
                payload_dict = json.loads(payload)
            except ValueError as e:
                raise InvalidJsonException(message=payload)

            if type(payload_dict) is dict:
                return payload
            else:
                raise InvalidJsonException(message=payload)
        else:
            raise InvalidJsonException(message=payload)
