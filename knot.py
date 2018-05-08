from proto import KnotProtocol

class KnotConnection(object):
	def __init__(self, protocol, credentials):
		self.protocol = KnotProtocol(protocol)
		self.credentials = credentials

	def registerDevice(self, user_data={}):
		result = self.protocol.registerDevice(self.credentials, user_data)
		return result

	def unregisterDevice(self, user_data={}):
		return self.protocol.unregisterDevice(self.credentials, user_data)

	def update(self, user_data={}):
		result = self.protocol.update(self.credentials, user_data)
		return result

	def myDevices(self):
		result = self.protocol.myDevices(self.credentials)
		if result.get('error'):
			raise Exception(result.get('error').get('message'))
		else:
			return result.get('devices')

	def getDevices(self):
		result = self.protocol.getDevices(self.credentials)
		if isinstance(result, dict) and result.get('Error'):
			raise Exception(result.get('Error'))
		else:
			return result

	def subscribe(self, uuid, onReceive=None):
		self.protocol.subscribe(self.credentials, uuid, onReceive)