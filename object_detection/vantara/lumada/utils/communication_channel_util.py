from lumada.utils.validator import Validator

class CommunicationChannelUtil:

    @staticmethod
    def add_cred_type_to_username(username = None):
        _cred_type = "devicehash"
        user = Validator.validate_param(username, 'username')
        cred_and_user = _cred_type + '.' + user
        return cred_and_user
