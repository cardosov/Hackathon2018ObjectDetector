"""
    Copyright (c) by Hitachi Data Systems, 2017. All rights reserved.
"""
from lumada.utils.validator import Validator


class LumadaEndpoint:

    def __init__(self, hostname=None, trust_certs=False, require_secure=True):
        """
        :param hostname: Hostname for the lumada endpoint
        :param trust_certs: (Optional) If set to True, will trust all certificates. Default is False
        """
        self._hostname = Validator.validate_param(hostname, 'hostname')
        self._trust_all_certs = trust_certs
        self._require_secure = require_secure

    def get_hostname(self):
        return self._hostname

    def get_require_secure(self):
        return self._require_secure

    def get_trust_all_certificates(self):
        return self._trust_all_certs
