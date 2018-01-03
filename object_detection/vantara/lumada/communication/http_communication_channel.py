from urllib.parse import quote
from lumada.communication.api.communication_channel_base import CommunicationChannelBase
from lumada.utils.http_util import HttpUtil
from lumada.utils.validator import Validator
from requests_toolbelt import StreamingIterator


class HttpCommunicationChannel(CommunicationChannelBase):
    UDS_FILES_URI_BASE = '/v1/unstructured-data/files'

    def __init__(self, communication_channel_config):
        self._http_util = HttpUtil(username=communication_channel_config.get_username(),
                                   password=communication_channel_config.get_password())
        self._channel_config = communication_channel_config

    def is_connected(self):
        """
        Checks the lumada /about api to see if there is connectivity
        :return: True if connected, False if /about returns a response code of 400+
        """
        endpoint_url = self._http_util.get_endpoint_url(hostname=self._channel_config.get_hostname(),
                                                        path='/v1/asset-connectivity/about',
                                                        params=None)
        try:
            response = self._http_util.request_json_response('get', endpoint_url)
        except Exception:
            return False

        if response:
            return True

    def connect(self):
        pass

    def disconnect(self):
        pass

    def publish(self, message):
        """
        Publish a message to the Lumada endpoint
        :param message: message to publish
        :return:
        """
        self._http_util.encode_creds(str(self._channel_config.get_username()), str(self._channel_config.get_password()))

        publish_url = self._get_publish_url(asset_id=message.get_asset_id(), gateway_id=message.get_gateway_id(),
                                            message_type=message.get_message_type(), message_name=message.get_message_name())

        response = self._http_util.request_json_response('post', publish_url, payload=message.get_payload(),
                                                         verify=self._channel_config.get_trust_certs())

    def _get_publish_url(self, asset_id=None, gateway_id=None, message_type=None, message_name=None, path=None):
        """
        Private: Returns a publishing URL
        :param asset_id: ID of the asset to publish
        :param gateway_id: ID of the gateway to publish
        :param message_type: Type of message to publish
        :param message_name: Name of message to publish
        :return: URL to post to
        """
        self.message_type = Validator.validate_param(message_type, 'message_type')
        self.asset_id = Validator.validate_param(asset_id, 'asset_id')

        if path is None:
            path = '/v1/asset-connectivity'

        if gateway_id is not None:
            path += '/gateways/%s/assets/%s/%s' % (str(gateway_id), str(asset_id), str(message_type))
        else:
            path += '/assets/%s/%s' % (str(asset_id), str(message_type))

        if message_name is not None:
            path += '/%s' % (str(message_name))

        publish_url = self._http_util.get_endpoint_url(hostname=self._channel_config.get_hostname(),
                                                       path=path, params=None)

        return publish_url

    def uds_file_put(self, asset_id, file_name, file_data, content_md5, additional_headers={}):
        """
        Uploads the file_data to uds
        :param file_data: an open, unread file object.  The file location should be at the beginning of the file data
        :return: the response object
        """
        self._http_util.encode_creds(str(self._channel_config.get_username()), str(self._channel_config.get_password()))

        additional_headers.update({'Content-MD5' : content_md5})

        # we have to perform the redirect manually, becuase the Requests library doesn't implement the 100-Continue
        # pattern; resulting in failed uploads for large files as the socket is closed after redirect while Requests is still uploading
        uds_url = self._get_uds_file_url(asset_id, file_name)
        uds_result = self._http_util.request(
            'put',
            uds_url,
            verify=self._channel_config.get_trust_certs(),
            allow_redirects=False,
            headers=additional_headers)

        redirect_url = uds_result.headers['Location']
        if not redirect_url:
            raise Exception("Unexpected response: " + uds_result.status_code)

        # remove Authorization header when following redirect
        additional_headers.update({'Authorization' : None})
        return self._http_util.request(
            'put',
            redirect_url,
            verify=self._channel_config.get_trust_certs(),
            data=file_data,
            headers=additional_headers)

    def uds_file_get(self, asset_id, file_name):
        """
        Retrieves the uds file
        :return: the response object
        """
        self._http_util.encode_creds(str(self._channel_config.get_username()), str(self._channel_config.get_password()))

        url = self._get_uds_file_url(asset_id, file_name)

        response = self._http_util.request('get', url, verify=self._channel_config.get_trust_certs(), stream=True)
        return response

    def uds_file_head(self, asset_id, file_name):
        """
        Retrieves the uds file headers
        :return: the response object
        """
        self._http_util.encode_creds(str(self._channel_config.get_username()), str(self._channel_config.get_password()))

        url = self._get_uds_file_url(asset_id, file_name)

        # by default HEAD requests do not follow redirects so we have to explicitly follow
        response = self._http_util.request('head', url, verify=self._channel_config.get_trust_certs(), allow_redirects=True)
        return response

    def uds_file_list(self, asset_id, prefix=None, marker=None):
        """
        Lists uds files associated with the asset
        :param prefix: limits the response to files that begin with the specified prefix
        :param marker: the file to start with when listing files for an asset
        :return: the response object
        """
        self._http_util.encode_creds(str(self._channel_config.get_username()), str(self._channel_config.get_password()))

        get_url = self._get_uds_list_url(asset_id, prefix, marker)

        response = self._http_util.request('get', get_url, verify=self._channel_config.get_trust_certs())
        return response

    def _get_uds_file_url(self, asset_id, file_name):
        path = '%s/%s/%s' % (str(self.UDS_FILES_URI_BASE), str(asset_id), quote(str(file_name)))
        return self._get_uds_url(path)

    def _get_uds_url(self, path, params=None):
        url = self._http_util.get_endpoint_url(hostname=self._channel_config.get_hostname(), path=path, params=params)
        return url

    def _get_uds_list_url(self, asset_id, prefix=None, marker=None):
        path = '%s/%s' % (str(self.UDS_FILES_URI_BASE), str(asset_id))
        params = {}
        if prefix:
            params.update({'prefix' : prefix})
        if marker:
            params.update({'marker' : marker})

        return self._get_uds_url(path, params)
