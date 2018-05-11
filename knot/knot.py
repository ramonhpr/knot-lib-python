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

	def postData(self, thing_uuid, user_data={}):
		return self.protocol.postData(self.credentials, thing_uuid, user_data)

	# The bellow methods just use in specific protocols
	def readData(self, thing_uuid, user_data={}):
		result = self.protocol.readData(self.credentials, thing_uuid, user_data)
		if result.get('error'):
			raise Exception(result.get('error'))
		else:
			return result.get('data')

	def setData(self, thing_uuid, sensor_id, value):
		properties = {
			'uuid': thing_uuid,
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}

		return self.protocol.update(self.credentials, properties)