
class ProtocolNotSupportedException:
  def __init__(self, **kwargs):
    self.message = kwargs.get('message')

  def __str__(self):
    return 'Protocol not supported: {0}'.format(self.message)