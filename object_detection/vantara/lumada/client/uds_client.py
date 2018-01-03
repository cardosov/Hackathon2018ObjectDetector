import base64
import hashlib

import xmltodict

from lumada.communication.http_communication_channel import HttpCommunicationChannel
from lumada.config.communication_channel_config import CommunicationChannelConfig
from lumada.contract.asset_communication_protocol import AssetCommunicationProtocol
from lumada.exception.protocol_not_supported_exception import ProtocolNotSupportedException
from lumada.utils.validator import Validator


class UdsClient:
  METADATA_HEADER_PREFIX = "x-amz-meta-"
  CONTENT_LENGTH_HEADER = "Content-Length"
  LAST_MODIFIED_HEADER = "Last-Modified"

  def __init__(self, lumada_client_config=None):
    self._communication_channel = self._create_lumada_communication_channel(
        Validator.validate_config_provided(lumada_client_config, 'LumadaClientConfig'))

  def file_put(self, asset_id, file_name, file_path, metadata={}):
    """
    Upload a file for the asset.
    :param asset_id: the asset id
    :param file_name: the name of the file.  This is the lumada name, not the local file name.
    :param file_path: the complete path to the file to upload for example: './myfile.txt' or '/files/myfile.txt'
    :return the response object
    """
    checksum = self._calculate_checksum(file_path)

    headers = {}
    for key, value in metadata.items():
      name = self.METADATA_HEADER_PREFIX + key
      headers[name] = value

    with open(file_path, 'rb') as data:
        return self._communication_channel.uds_file_put(asset_id, file_name, data, checksum, headers)

  def file_get(self, asset_id, file_name):
    """
    Retrieve an assets file.
    :param asset_id: the asset id
    :param file_name: the file name
    :return the response object
    """
    return self._communication_channel.uds_file_get(asset_id, file_name)

  def file_metadata_get(self, asset_id, file_name):
    """
    Retrieve the metadata for an assets file.
    :param asset_id: the asset id
    :param file_name: the file name
    :return the file metadata
    """
    result = self._communication_channel.uds_file_head(asset_id, file_name)
    metadata = { "Name" : file_name, "AssetId" : asset_id }
    custom_metadata = {}
    for key, value in result.headers.items():
      if self._case_insensitive_equals(self.CONTENT_LENGTH_HEADER, key):
        metadata["Size"] = value
      elif self._case_insensitive_equals(self.LAST_MODIFIED_HEADER, key):
        metadata["LastModified"] = value
      elif self._case_insensitive_starts_with(prefix=self.METADATA_HEADER_PREFIX, target=key):
        name = self._strip_prefix(self.METADATA_HEADER_PREFIX, key)
        custom_metadata[name] = value

    metadata['CustomMetadata'] = custom_metadata
    return metadata

  def file_list(self, asset_id, prefix=None, marker=None):
    """
    Retrieve the assets file listing.
    :param asset_id: the asset id
    :param prefix: Limits the response to file names that begin with the specified prefix
    :param marker: Specifies the file name to start from when listing files for an asset
    :return the list result
    """
    result = self._communication_channel.uds_file_list(asset_id, prefix, marker)
    result_dict = xmltodict.parse(result.text)

    s3_list_result = result_dict['ListBucketResult']
    list_result = {}
    list_result['Prefix'] = self._strip_slash_delimited_prefix(asset_id, s3_list_result['Prefix'])
    list_result['Marker'] = self._strip_slash_delimited_prefix(asset_id, s3_list_result['Marker'])
    list_result['IsTruncated'] = s3_list_result['IsTruncated']
    list_result['AssetId'] = asset_id

    files = []
    for entry in s3_list_result['Contents'] :
      name = self._strip_slash_delimited_prefix(asset_id, entry['Key'])
      files.append({'Name' : name, 'LastModified' : entry['LastModified'], "Size": entry['Size']})
    list_result['Contents'] = files

    return list_result

  def _strip_slash_delimited_prefix(self, prefix, target):
    """
    If target starts with prefix/, the remainder of target following prefix/ is returned
    :param prefix: the prefix that target starts with
    :param target: the target string
    :return: the remainder of target following prefix/
    """
    return self._strip_prefix(prefix + '/', target)

  def _case_insensitive_equals(self, expected, actual):
    """
    True if target str(actual).lower() == str(expected).lower()
    :param expected: the expected string
    :param actual: the string to check
    """
    return str(expected).lower() == str(actual).lower()

  def _case_insensitive_starts_with(self, prefix, target):
    """
    True if str(target).lower().startswith(str(prefix).lower())
    :param target: the string to check
    :param prefix: the prefix to check for
    """
    return str(target).lower().startswith(str(prefix).lower())

  def _strip_prefix(self, prefix, target):
    """
    If target starts with prefix, the remainder of target following prefix is returned
    :param prefix: the prefix that target starts with
    :param target: the target string
    :return: the remainder of target following prefix/
    """
    if str(target).startswith(prefix):
      return target.split('/', 1)[1]

  def _create_lumada_communication_channel(self, client_config):
    """
    Helper to create communication channel from the provided config.
    """
    channel_config = CommunicationChannelConfig(hostname=client_config.get_asset_endpoint().get_hostname(),
                                                username=client_config.get_credentials().get_entity_id(),
                                                password=client_config.get_credentials().get_entity_value(),
                                                trust_certs=client_config.get_asset_endpoint().get_trust_all_certificates(),
                                                requires_secure=client_config.get_asset_endpoint().get_require_secure())

    if client_config.get_protocol() == AssetCommunicationProtocol.HTTP:
      return HttpCommunicationChannel(channel_config)
    else:
      raise ProtocolNotSupportedException(client_config.get_protocol())

  def _calculate_checksum(self, file_path, blocksize=2**20):
    digestor = hashlib.md5()
    with open(file_path, 'rb') as data:
      while True:
        buf = data.read(blocksize)
        if not buf:
          break
        digestor.update(buf)
    digest = digestor.digest()
    encoded = base64.encodebytes(digest)
    # turns bytes into utf-8 string and remove trailing newline
    return encoded.decode("utf-8").rstrip()

