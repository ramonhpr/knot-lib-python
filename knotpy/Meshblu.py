import logging
import functools
from uuid import UUID
from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
from .handler import handleResponseError
from .Cloud import Cloud
from .decorators import omit
__all__=[]

# Device parameters to be omitted
DEVICE_PARAMS = [
	'_id',
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
	'set_data']

REGISTERED_PARAMS = list(DEVICE_PARAMS)
REGISTERED_PARAMS.remove('token') # don't omit token in register

def getDeviceUuid(devices, device_id):
	try:
		device = [d for d in devices if d.get('id') == device_id][0]
	except IndexError as err:
		raise IndexError('Device not found')
	return device.get('uuid')

def useUuid(func):
	@functools.wraps(func)
	def func_wrapper(self, credentials, device_id, *args, **kwargs):
		devices = ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']})
		uuid = getDeviceUuid(devices, device_id)
		return func(self, credentials, uuid, *args, **kwargs)
	return func_wrapper

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

	@omit(REGISTERED_PARAMS)
	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		try: # validate if uuid is in the right format
			UUID(credentials.get('uuid'), version=4)
		except ValueError as err:
			raise ValueError('Invalid credentials: ' + str(err))
		return self.protocol.registerDevice(credentials, properties)

	@useUuid
	@omit(DEVICE_PARAMS)
	def unregisterDevice(self, credentials, device_id, user_data={}):
		return handleResponseError(self.protocol.unregisterDevice(device_id, credentials, user_data))

	@omit(DEVICE_PARAMS)
	def myDevices(self, credentials):
		return handleResponseError(self.protocol.myDevices(credentials)).get('devices')

	@useUuid
	def subscribe(self, credentials, device_id, onReceive=None):
		self.protocol.subscribe(credentials, device_id, onReceive)

	@useUuid
	@omit(DEVICE_PARAMS)
	def update(self, credentials, device_id, user_data={}):
		properties = {'uuid': device_id}
		properties.update(user_data)
		return handleResponseError(self.protocol.update(credentials, device_id, properties))

	@useUuid
	@omit(DEVICE_PARAMS)
	def getData(self, credentials, device_id, **kwargs):
		return self.protocol.getData(credentials, device_id, **kwargs)

	@useUuid
	@omit(DEVICE_PARAMS)
	def postData(self, credentials, device_id, user_data={}):
		properties = {'uuid': device_id}
		properties.update(user_data)
		return self.protocol.postData(credentials, device_id, properties)

	@omit(DEVICE_PARAMS)
	def listSensors(self, credentials, device_id):
		devices = ProtoSocketio().getDevices(credentials,
							{'gateways': ['*']})
		uuid = getDeviceUuid(devices, device_id)
		schema = [dev.get('schema') for dev in devices if dev.get('uuid') == uuid][0]
		try:
			return [sensor.get('sensor_id') for sensor in schema]
		except KeyError as err:
			return []

	@omit(DEVICE_PARAMS)
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

	@omit(DEVICE_PARAMS)
	def getThings(self, credentials, gateways=['*']):
		logging.warn('This function is using protocol socketio')
		properties = {
			'gateways': gateways
		}
		return handleResponseError(ProtoSocketio().getDevices(credentials, properties))

	@useUuid
	@omit(DEVICE_PARAMS)
	def setData(self, credentials, device_id, sensor_id, value):
		properties = {
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return handleResponseError(ProtoSocketio().update(credentials, device_id, properties))

	@useUuid
	@omit(DEVICE_PARAMS)
	def requestData(self, credentials, device_id, sensor_id):
		properties = {
			'get_data': [{
				'sensor_id': sensor_id
				}]
		}
		return handleResponseError(ProtoSocketio().update(credentials, device_id, properties))

	@useUuid
	@omit(DEVICE_PARAMS)
	def setConfig(self, credentials, device_id, sensor_id, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
		properties = {
			'config': [{
				'sensor_id': sensor_id,
				'event_flags': eventFlags,
				'time_sec': timeSec,
				'lower_limit': lowerLimit,
				'upper_limit': upperLimit
				}]
		}
		return handleResponseError(ProtoSocketio().update(credentials, device_id, properties))
