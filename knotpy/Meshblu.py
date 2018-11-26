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
	'uuid',
	'token',
	'meshblu',
	'discoverWhitelist',
	'configureWhitelist',
	'socketid',
	'secure',
	'get_data',
	'schema',
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

def getDeviceUuid(devices, device_id):
	try:
		device = [d for d in devices if d.get('id') == device_id][0]
	except IndexError as err:
		raise IndexError('Device not found')
	return device.get('uuid')

def authHttpHeaders(credentials):
	return {
		'meshblu_auth_uuid': credentials.get('uuid'),
		'meshblu_auth_token': credentials.get('token')
	}

class Meshblu(object):
	def __init__(self, protocol):
		logging.info('Using protocol ' + protocol)
		self.protocol = {
			'socketio': lambda: ProtoSocketio(),
			'http': lambda: ProtoHttp(headers=authHttpHeaders,
				addDev=lambda: {'type': 'POST', 'endpoint':'/devices'},
				listDev=lambda: {'type': 'GET', 'endpoint':'/mydevices'},
				rmDev=lambda uuid: {'type': 'DELETE', 'endpoint':'/devices/%s' %uuid},
				updateDev=lambda uuid: {'type': 'PUT', 'endpoint':'/devices/%s' %uuid},
				addData=lambda uuid: {'type': 'POST', 'endpoint': '/data/%s' %uuid},
				listData=lambda uuid: {'type': 'GET', 'endpoint': '/data/%s' %uuid},
				subs=lambda uuid: {'type': 'GET', 'endpoint': '/subscribe/%s' %uuid})
		}.get(protocol.lower())()

	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		try: # validate if uuid is in the right format
			UUID(credentials.get('uuid'), version=4)
		except ValueError as err:
			raise ValueError('Invalid credentials: ' + str(err))
		return omitDeviceRegisteredParameters(self.protocol.registerDevice(credentials, properties))

	def unregisterDevice(self, credentials, device_id, user_data={}):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		return omitDeviceParameters(handleResponseError(self.protocol.unregisterDevice(credentials, uuid, user_data)))

	def myDevices(self, credentials):
		return omitDevicesParameters(handleResponseError(self.protocol.myDevices(credentials)).get('devices'))

	def subscribe(self, credentials, device_id, onReceive=None):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		self.protocol.subscribe(credentials, uuid, onReceive)

	def update(self, credentials, device_id, user_data={}):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		properties = {'uuid': uuid}
		properties.update(user_data)
		return omitDeviceParameters(handleResponseError(self.protocol.update(credentials, uuid, properties)))

	def getData(self, credentials, device_id, **kwargs):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		return self.protocol.getData(credentials, uuid, **kwargs)

	def postData(self, credentials, device_id, user_data={}):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		properties = {'uuid': uuid}
		properties.update(user_data)
		return self.protocol.postData(credentials, uuid, properties)

	def listSensors(self, credentials, device_id):
		devices = ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']})
		uuid = getDeviceUuid(devices, device_id)
		schema = [dev.get('schema') for dev in devices if dev.get('uuid') == uuid][0]
		try:
			return [sensor.get('sensor_id') for sensor in schema]
		except KeyError as err:
			return []

	def getSensorDetails(self, credentials, device_id, sensor_id):
		deviceSchema = []
		devices = ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']})
		uuid = getDeviceUuid(devices, device_id)
		try:
			deviceSchema = [dev for dev in devices if dev.get('uuid') == uuid][0]['schema']
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

	def setData(self, credentials, device_id, sensor_id, value):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		properties = {
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, uuid, properties)))

	def requestData(self, credentials, device_id, sensor_id):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		properties = {
			'get_data': [{
				'sensor_id': sensor_id
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, uuid, properties)))

	def setConfig(self, credentials, device_id, sensor_id, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
		uuid = getDeviceUuid(ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']}), device_id)
		properties = {
			'config': [{
				'sensor_id': sensor_id,
				'event_flags': eventFlags,
				'time_sec': timeSec,
				'lower_limit': lowerLimit,
				'upper_limit': upperLimit
				}]
		}
		return omitDeviceParameters(handleResponseError(ProtoSocketio().update(credentials, uuid, properties)))
