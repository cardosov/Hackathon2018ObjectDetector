"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.utils.validator import Validator


class CommunicationChannelConfig:

    def __init__(self, hostname=None, username=None, password=None, requires_secure=True, trust_certs=False):
        self._hostname = Validator.validate_param(hostname, 'hostname')
        self._username = Validator.validate_param(username, 'username')
        self._password = Validator.validate_param(password, 'password')
        self._requires_secure = requires_secure
        self._trust_certs = trust_certs
        self._exchange = 'lumada'

    def get_hostname(self):
        return self._hostname

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_requires_secure(self):
        return self._requires_secure

    def get_trust_certs(self):
        return self._trust_certs

    def get_exchange(self):
        return self._exchange
