from .cloud_factory import CloudFactory
from .handler import *
from .evt_flag import *
__all__ = ['KnotConnection']

class KnotConnection(object):
	'''This is the main class to connect to KNoT Cloud
	KnotConnection(credentials, protocol='http')
	'''
	def __init__(self, credentials, cloud='MESHBLU', protocol='socketio'):
		self.cloud = CloudFactory.init(cloud, protocol)
		self.credentials = credentials

	def registerDevice(self, user_data={}):
		'''
		Register a device in the cloud with owner credentials
		and return a dict/json with the device added
		'''
		result = self.cloud.registerDevice(self.credentials, user_data)
		return result

	def unregisterDevice(self, device_id, user_data={}):
		'''
		Unregister a device with the credentials passed by the dict/json
		parameter and return the successed json message
		'''
		result = self.cloud.unregisterDevice(self.credentials, device_id, user_data)
		return handleResponseError(result)

	def update(self, device_id, user_data={}):
		'''
		Update a device with the credentials passed by the dict/json
		parameter and return the successed json message
		'''
		result = self.cloud.update(self.credentials, device_id, user_data)
		return handleResponseError(result)

	def myDevices(self):
		'''
		Return all devices of your gateway
		Note:
			If you run it in the cloud it returns the gateway device
			If you run it in the fog it returns all the devices of your gateway
		'''
		result = self.cloud.myDevices(self.credentials)
		return handleResponseError(result)

	def subscribe(self, device_id, onReceive=None):
		'''
		Subscribe the device to monitor changes on it
		'''
		self.cloud.subscribe(self.credentials, device_id, onReceive)

	def postData(self, device_id, user_data={}):
		'''
		Post the json passed in user_data to the cloud
		'''
		return self.cloud.postData(self.credentials, device_id, user_data)

	def getData(self, device_id, **kwargs):
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
		result = self.cloud.getData(self.credentials, device_id, **kwargs)
		data = handleResponseError(result).get('data')
		return data

	# The bellow methods just use in specific protocols
	def listSensors(self, thing_uuid):
		return self.cloud.listSensors(self.credentials, thing_uuid)

	def getSensorDetails(self, thing_uuid, sensor_id):
		return self.cloud.getSensorDetails(self.credentials, thing_uuid, sensor_id)

	def getThings(self):
		'''
		Get the things of your user
		'''
		result = self.cloud.getThings(self.credentials)
		return handleResponseError(result)

	def setData(self, device_id, sensor_id, value):
		'''
		Set data of the sensor from your thing
		'''
		result = self.cloud.setData(self.credentials, device_id, sensor_id, value)
		return handleResponseError(result)

	def requestData(self, device_id, sensor_id):
		'''
		Force your thing to post sensor data indepent of your configuration
		'''
		result = self.cloud.requestData(self.credentials, device_id, sensor_id)
		data = handleResponseError(result)
		return data

	def sendConfig(self, device_id, sensor_id, eventFlags=FLAG_CHANGE, timeSec=0,
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
		result = self.cloud.setConfig(self.credentials, device_id, sensor_id,
									 eventFlags, timeSec, lowerLimit, upperLimit)
		return handleResponseError(result)
