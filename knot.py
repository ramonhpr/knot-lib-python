from proto import KnotProtocol

class KnotConnection(object):
	def __init__(self, protocol, credentials):
		self.protocol = KnotProtocol(protocol)
		self.credentials = credentials

	def getDevices(self):
		result = self.protocol.getDevices(self.credentials)
		if isinstance(result, dict) and result.get('Error'):
			raise Exception(result.get('Error'))
		else:
			return result