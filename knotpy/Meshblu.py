import logging
from uuid import UUID
from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
from .handler import handleResponseError
from .Cloud import Cloud
__all__=[]

def _omit(json, arr):
	return {k: v for k,v in json.items() if k not in arr}

def omitDeviceParameters(device):
	return _omit(device,['_id',
	'owner',
	'type',
	'ipAddress',
	'token',
	'meshblu',
	'discoverWhitelist',
	'configureWhitelist',
	'socketid',
	'secure',
	'get_data',
	'set_data'])

def omitDeviceRegisteredParameters(device):
	return _omit(device,['_id',
	'owner',
	'type',
	'ipAddress',
	'meshblu',
	'discoverWhitelist',
	'configureWhitelist',
	'socketid',
	'secure',
	'get_data',
	'set_data'])

def omitDevicesParameters(devices):
	for i,dev in enumerate(devices):
		devices[i] = omitDeviceParameters(dev)
	return devices

def authHttpHeaders(credentials):
	return {
		'meshblu_auth_uuid': credentials.get('uuid'),
		'meshblu_auth_token': credentials.get('token')
	}

def addDevice():
	return {'type': 'POST', 'endpoint':'/devices'}

def rmDevice(uuid):
	return {'type': 'DELETE', 'endpoint':'/devices/%s' %uuid}

def listDevice():
	return {'type': 'GET', 'endpoint':'/mydevices'}

def updateDevice(uuid):
	return {'type': 'PUT', 'endpoint':'/devices/%s' %uuid}

def listData(uuid):
	return {'type': 'GET', 'endpoint': '/data/%s' %uuid}

def addData(uuid):
	return {'type': 'POST', 'endpoint': '/data/%s' %uuid}

def subs(uuid):
	return {'type': 'GET', 'endpoint': '/subscribe/%s' %uuid}

class Meshblu(Cloud):
	def __init__(self, protocol):
		logging.info('Using protocol ' + protocol)
		self.protocol = {
			'socketio': ProtoSocketio(),
			'http': ProtoHttp(headers=authHttpHeaders,
							addDev=addDevice,
							rmDev=rmDevice,
							listDev=listDevice,
							updateDev=updateDevice,
							addData=addData,
							listData=listData,
							subs=subs)
		}.get(protocol.lower())

	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		try: # validate if uuid is in the right format
			UUID(credentials.get('uuid'), version=4)
		except ValueError as err:
			raise ValueError('Invalid credentials: ' + str(err))
		return omitDeviceRegisteredParameters(self.protocol.registerDevice(credentials, properties))

	def unregisterDevice(self, credentials, uuid, user_data={}):
		return omitDeviceParameters(handleResponseError(self.protocol.unregisterDevice(credentials, uuid, user_data)))

	def myDevices(self, credentials):
		return omitDevicesParameters(handleResponseError(self.protocol.myDevices(credentials).get('devices')))

	def subscribe(self, credentials, uuid, onReceive=None):
		self.protocol.subscribe(credentials, uuid, onReceive)

	def update(self, credentials, uuid, user_data={}):
		if not isinstance(uuid, str):
			raise Exception('uuid is required')
		if not uuid:
			raise Exception('uuid is required')
		properties = {'uuid': uuid}
		properties.update(user_data)
		return omitDeviceParameters(handleResponseError(self.protocol.update(credentials, uuid, properties)))

	def getData(self, credentials, thing_uuid, **kwargs):
		return self.protocol.getData(credentials, thing_uuid, **kwargs)

	def postData(self, credentials, thing_uuid, user_data={}):
		properties = {'uuid': thing_uuid}
		properties.update(user_data)
		return self.protocol.postData(credentials, thing_uuid, properties)

	def listSensors(self, credentials, thing_uuid):
		device = [dev for dev in self.getThings(credentials) if dev.get('uuid') == thing_uuid][0]
		try:
			return [i.get('sensor_id') for i in device['schema']]
		except KeyError as err:
			return []

	def getSensorDetails(self, credentials, thing_uuid, sensor_id):
		deviceSchema = []
		try:
			deviceSchema = [dev for dev in self.getThings(credentials) if dev.get('uuid') == thing_uuid][0]['schema']
		except Exception as err:
			raise Exception('None sensor is registered in this thing')

		if len(deviceSchema) > 0:
			try:
				return [sensor for sensor in deviceSchema if sensor.get('sensor_id') == sensor_id][0]
			except IndexError as err:
				raise Exception('This thing has not this sensor id')
		else:
			raise Exception('None sensor is registered in this thing')

	def getThings(self, credentials, gateways=['*']):
		logging.warn('This function is using protocol socketio')
		properties = {
			'gateways': gateways
		}
		return omitDevicesParameters(handleResponseError(ProtoSocketio().getDevices(credentials, properties)))

	def setData(self, credentials, thing_uuid, sensor_id, value):
		logging.warn('This function is using protocol socketio')
		properties = {
			'uuid': thing_uuid,
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, properties)))

	def requestData(self, credentials, thing_uuid, sensor_id):
		logging.warn('This function is using protocol socketio')
		properties = {
			'uuid': thing_uuid,
			'get_data': [{
				'sensor_id': sensor_id
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, properties)))

	def setConfig(self, credentials, thing_uuid, sensor_id, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
		logging.warn('This function is using protocol socketio')
		properties = {
			'uuid': thing_uuid,
			'config': [{
				'sensor_id': sensor_id,
				'event_flags': eventFlags,
				'time_sec': timeSec,
				'lower_limit': lowerLimit,
				'upper_limit': upperLimit
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, properties)))