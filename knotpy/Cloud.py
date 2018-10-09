class Cloud(object):
	def registerDevice(self, credentials, user_data={}):
		pass
	def unregisterDevice(self, credentials, uuid, user_data={}):
		pass
	def myDevices(self, credentials):
		pass
	def subscribe(self, credentials, uuid, onReceive=None):
		pass
	def update(self, credentials, uuid, user_data={}):
		pass
	def getData(self, credentials, thing_uuid, **kwargs):
		pass
	def postData(self, credentials, thing_uuid, user_data={}):
		pass
	def listSensors(self, credentials, thing_uuid):
		pass
	def getSensorDetail(self, credentials, thing_uuid, sensor_id):
		pass
	def getThings(self, credentials, gateways=['*']):
		pass
	def setData(self, credentials, thing_uuid, sensor_id, value):
		pass
	def requestData(self, credentials, thing_uuid, sensor_id):
		pass
	def setConfig(self, credentials, thing_uuid, sensor_id,
					eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
		pass