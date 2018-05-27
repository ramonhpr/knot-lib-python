from .proto import KnotProtocol
from .evt_flag import EvtFlagsEnum
from .handler import *

class KnotConnection(object):
	def __init__(self, protocol, credentials):
		self.protocol = KnotProtocol(protocol)
		self.credentials = credentials

	def registerDevice(self, user_data={}):
		result = self.protocol.registerDevice(self.credentials, user_data)
		return result

	def unregisterDevice(self, user_data={}):
		result = self.protocol.unregisterDevice(self.credentials, user_data)
		return handleResponseError(result)

	def update(self, uuid, user_data={}):
		result = self.protocol.update(self.credentials, uuid, user_data)
		return handleResponseError(result)

	def myDevices(self):
		result = self.protocol.myDevices(self.credentials)
		devices = handleResponseError(result).get('devices')
		return devices

	def subscribe(self, uuid, onReceive=None):
		self.protocol.subscribe(self.credentials, uuid, onReceive)

	def postData(self, thing_uuid, user_data={}):
		return self.protocol.postData(self.credentials, thing_uuid, user_data)

	# The bellow methods just use in specific protocols

	def getThings(self):
		result = self.protocol.getThings(self.credentials)
		return handleResponseError(result)

	def readData(self, thing_uuid, **kwargs): 
		result = self.protocol.readData(self.credentials, thing_uuid, **kwargs)
		data = handleResponseError(result).get('data')
		return data

	def setData(self, thing_uuid, sensor_id, value):
		result = self.protocol.setData(self.credentials, thing_uuid, sensor_id, value)
		return handleResponseError(result)

	def getData(self, thing_uuid, sensor_id):
		result = self.protocol.getData(self.credentials, thing_uuid, sensor_id)
		data = handleResponseError(result)
		return data

	def setConfig(self, thing_uuid, sensor_id, eventFlags=8, timeSec=0,
					 lowerLimit=0, upperLimit=0):
		handleEvtFlagError(eventFlags, timeSec, lowerLimit, upperLimit)
		result = self.protocol.setConfig(self.credentials, thing_uuid, sensor_id,
									 eventFlags, timeSec, lowerLimit, upperLimit)
		return handleResponseError(result)
