from enum import Enum


class LumadaMessageType(Enum):
    """
    Message types supported by lumada
    """
    EVENT = 'event'
    STATE = 'state'
