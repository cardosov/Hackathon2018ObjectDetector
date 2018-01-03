"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.utils.validator import Validator


class EntityCredentials:

    def __init__(self, entity_id=None, entity_value=None):
        self._entity_id = Validator.validate_param(entity_id, 'entity_id')
        self._entity_value = Validator.validate_param(entity_value, 'entity_value')

    def get_entity_id(self):
        """
        Provides the Lumada entity_id from the credentials.
        :return: the Lumada entity_id.
        """
        return self._entity_id

    def get_entity_value(self):
        """
        Provides the Lumada entity_value that will be used for authentication.
        :return: the Lumada entity_value.
        """
        return self._entity_value
