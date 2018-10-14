class Protocol(object):
	def registerDevice(self, credentials, user_data={}):
		pass
	def unregisterDevice(self, credentials, device_id, user_data={}):
		pass
	def myDevices(self, credentials, user_data={}):
		pass
	def subscribe(self, credentials, device_id, onReceive=None):
		pass
	def update(self, credentials, device_id, user_data={}):
		pass
	def postData(self, credentials, device_id, user_data={}):
		pass
	def getData(self, credentials, device_id, **kwargs):
		pass