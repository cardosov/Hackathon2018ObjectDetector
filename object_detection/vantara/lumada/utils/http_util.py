import requests
import urllib.parse
import json
import base64
from lumada.exception.data_not_serializable_exception import DataNotSerializableException
from lumada.utils.validator import Validator


class HttpUtil(object):
    """
    This class manages the http connection to lumada
    It is partially a wrapper around requests
    Authorization is also handled here
    """

    def __init__(self, username, password):
        """
        Initializes requests session with lumada
        :param username: user to authenticate to lumada
        :param password: password to authenticate to lumada
        """
        self.session = requests.session()

        Validator.validate_param(username, 'username')
        Validator.validate_param(password, 'password')

        self._username = username
        self._password = password

        self.encode_creds(username=username, password=password)

    def _request(self, method, url, verify=False, **kwargs):
        """
        Sends a post request to lumada
        :param kwargs: passed in unmodified to requests
        :raises UnicodeDecodeError: Error if response is not json
        :return: dict representation of json API response
        """
        if method == "post":
            kwargs.setdefault('headers', {}).update({'Content-Type' : 'application/json'})
            response = self.session.post(url, data=kwargs['payload'], verify=verify, headers=kwargs['headers'])
        elif method == "get":
            response = self.session.get(url, verify=verify, **kwargs)
        elif method == "head":
            response = self.session.head(url, verify=verify, **kwargs)
        elif method == "delete":
            response = self.session.get(url, verify=verify)
        elif method == "put":
            kwargs.setdefault('headers', {}).update({'Content-Type' : 'application/octet-stream'})
            response = self.session.put(url, verify=verify, **kwargs)
        #add additional verbs here

        # raises exception if there is an error response code (e.g. 400s or 500s)
        if not response.ok:
            print("failure reason " + response.text)
            response.raise_for_status()

        return response

    def request_json_response(self, method, url, verify=False, **kwargs):
        """
        Performs the request and returns a dict representation of the json response.
        If the response is not valid json, the response status message (i.e. OK) is returned
        :param method: http verb to send the request
        :param verify: allow self-signed certificate, default is to disallow (True)
        :param kwargs: args unmodified passed into python requests
        :return: dict representation of API json response or response status message
        :raises: HTTPError if there is an error response code (e.g. 400s or 500s)
        """
        response = self._request(method, url, verify, **kwargs)
        try:
            response = response.json()
        except ValueError as e:
            response = response.reason

        return response

    def request(self, method, url, verify=False, **kwargs):
        """
        Performs the request and returns the response object
        :param method: http verb to send the request
        :param verify: allow self-signed certificate, default is to disallow (True)
        :param kwargs: args unmodified passed into python requests
        :return: the response object
        :raises: HTTPError if there is an error response code (e.g. 400s or 500s)
        """
        return self._request(method, url, verify, **kwargs)

    def get_endpoint_url(self, hostname, path, params):
        """
        Creates url for desired request to lumada
        :param hostname: hostname to make the request
        :param port: port to make the request against
        :param path: path of the url to make the request
        :return: generated endpoint url
        """
        endpoint_url = URL(hostname=hostname, path=path, params=params)
        return endpoint_url

    def encode_creds(self, username=None, password=None):
        """
        Encodes http header for lumada of the form:
        {'Authorization ' : 'devicehash.<assetid>'}
        updates requests session header with the header
        :param username: Username to encode
        :param password: Password to encode
        """

        auth_header = {}
        auth_header['entityId'] = username
        auth_header['entityValue'] = password

        # do not use JsonUtil here, as Utils should be independent of each other
        try:
            auth_header_json = json.dumps(auth_header)
        except(TypeError):
            raise DataNotSerializableException(message='Asset payload is not serializable, payload sent %s'
                                                % (auth_header))

        #force encoding of json string to utf-8 for the base64 encoder
        auth_header_encoded = base64.b64encode(auth_header_json.encode('utf-8'))
        self.session.headers.update({'Authorization' : 'devicehash {0}'.format(auth_header_encoded.decode('utf-8'))})



#If there is a better way or a stdlib to build a url, this will be replaced
class URL:

    def __init__(self, hostname, port=None, path=None, params=None, **kwargs):
        """
        Builds a URL with the following parameters
        :param hostname: hostname of the url
        :param port: port for the url
        :param path: path to be appended at the end of the url
        :return: A URL string
        """
        self.hostname = hostname
        self.port = port
        self.path = path
        self.params = params

    def __str__(self):
        url = "https://"
        url += self.hostname
        if self.port is not None:
            url += ":" + str(self.port)
        if self.path is None:
            url += "/v1/asset-management"
        if self.path is not None:
            url += self.path
        if self.params:
            url += '?'
            url += URL.encode_parameters(params=self.params)
        return url

    @staticmethod
    def encode_parameters(params):
        path = urllib.parse.urlencode(params)
        return path
