from .proto import KnotProtocol
from .handler import *
from .evt_flag import *
__all__ = ['KnotConnection']

class KnotConnection(object):
	'''This is the main class to connect to KNoT Cloud
	KnotConnection(protocol, credentials)
	'''
	def __init__(self, protocol, credentials):
		self.protocol = KnotProtocol(protocol)
		self.credentials = credentials

	def registerDevice(self, user_data={}):
		'''
		Register a device in the cloud with owner credentials
		and return a dict/json with the device added
		'''
		result = self.protocol.registerDevice(self.credentials, user_data)
		return result

	def unregisterDevice(self, user_data={}):
		'''
		Unregister a device with the credentials passed by the dict/json
		parameter and return the successed json message
		'''
		result = self.protocol.unregisterDevice(self.credentials, user_data)
		return handleResponseError(result)

	def update(self, uuid, user_data={}):
		'''
		Update a device with the credentials passed by the dict/json
		parameter and return the successed json message
		'''
		result = self.protocol.update(self.credentials, uuid, user_data)
		return handleResponseError(result)

	def myDevices(self):
		'''
		Return all devices of your gateway
		Note:
			If you run it in the cloud it returns the gateway device
			If you run it in the fog it returns all the devices of your gateway
		'''
		result = self.protocol.myDevices(self.credentials)
		devices = handleResponseError(result).get('devices')
		return devices

	def subscribe(self, uuid, onReceive=None):
		'''
		Subscribe the device to monitor changes on it
		'''
		self.protocol.subscribe(self.credentials, uuid, onReceive)

	def postData(self, thing_uuid, user_data={}):
		'''
		Post the json passed in user_data to the cloud
		'''
		return self.protocol.postData(self.credentials, thing_uuid, user_data)

	def getData(self, thing_uuid, **kwargs):
		'''
		Get thing data from cloud and
		return a list of dict/json with your data
		You can pass querys to this function by using:
			- limit: the maximum number of data that you want, default=10
			- start: the start date that you want your set of data
			- finish: the finish date that you want your set of data
		Examples:
		conn.getData(thing_uuid, limit=20, start='yesterday') # get 20 first data from yesterday
		conn.getData(thing_uuid, limit=1) # get most recent data from your sensor
		conn.getData(thing_uuid, finish='2018/03/15') # get data the 10 data from until this date
		'''
		result = self.protocol.readData(self.credentials, thing_uuid, **kwargs)
		data = handleResponseError(result).get('data')
		return data

	# The bellow methods just use in specific protocols

	def getThings(self):
		'''
		Get the things of your user
		'''
		result = self.protocol.getThings(self.credentials)
		return handleResponseError(result)

	def setData(self, thing_uuid, sensor_id, value):
		'''
		Set data of the sensor from your thing
		'''
		result = self.protocol.setData(self.credentials, thing_uuid, sensor_id, value)
		return handleResponseError(result)

	def sendGetData(self, thing_uuid, sensor_id):
		'''
		Force your thing to post sensor data indepent of your configuration
		'''
		result = self.protocol.getData(self.credentials, thing_uuid, sensor_id)
		data = handleResponseError(result)
		return data

	def sendConfig(self, thing_uuid, sensor_id, eventFlags=FLAG_CHANGE, timeSec=0,
					 lowerLimit=0, upperLimit=0):
		'''
		Send configuration from the sensor of your thing if it is online
		You can use the event flags macro bellow:
		FLAG_TIME
		FLAG_LOWER
		FLAG_UPPER
		FLAG_CHANGE
		FLAG_MAX
		'''
		handleEvtFlagError(eventFlags, timeSec, lowerLimit, upperLimit)
		result = self.protocol.setConfig(self.credentials, thing_uuid, sensor_id,
									 eventFlags, timeSec, lowerLimit, upperLimit)
		return handleResponseError(result)
