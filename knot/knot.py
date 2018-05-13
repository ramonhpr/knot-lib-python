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
		return self.protocol.setData(self.credentials, thing_uuid, sensor_id, value)

	def getData(self, thing_uuid, sensor_id):
		return self.protocol.getData(self.credentials, thing_uuid, sensor_id)
	
	def setConfig(self, thing_uuid, sensor_id, eventFlags=8, timeSec=0,
					 lowerLimit=0, upperLimit=0):
		# TODO: Make a enum to map the eventFlags
		return self.protocol.setConfig(self.credentials, thing_uuid, sensor_id,
									 eventFlags, timeSec, lowerLimit, upperLimit)