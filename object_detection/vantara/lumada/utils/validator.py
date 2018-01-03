from lumada.exception.missing_config_exception import MissingConfigException
from lumada.exception.missing_param_exception import MissingParamException

class Validator:

    @staticmethod
    def validate_param(param, param_name):
        if param is None:
            raise MissingParamException(message="Missing params value for %s." % param_name)

        return param

    @staticmethod
    def validate_config_provided(config, config_name):
        if config is None:
            raise MissingConfigException(message="Missing configuration for %s." % config_name)

        return config
