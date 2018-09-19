from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
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

def omitDevicesParameters(devices):
	for i,dev in enumerate(devices):
		devices[i] = omitDeviceParameters(dev)
	return devices

class KnotProtocol(object):
	def __init__(self, protocol):
		self.protocol = {
			'socketio': ProtoSocketio(),
			'http': ProtoHttp()
		}.get(protocol)

	def __str__(self):
		return 'http' if isinstance(self.protocol, ProtoHttp) else 'socketio'

	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		return self.protocol.registerDevice(credentials, properties)

	def unregisterDevice(self, credentials,user_data={}):
		return self.protocol.unregisterDevice(credentials, user_data)

	def myDevices(self, credentials):
		return omitDevicesParameters(self.protocol.myDevices(credentials).get('devices'))

	def subscribe(self, credentials, uuid, onReceive=None):
		self.protocol.subscribe(credentials, uuid, onReceive)

	def update(self, credentials, uuid, user_data={}):
		if not isinstance(uuid, str):
			raise Exception('uuid is required')
		if not uuid:
			raise Exception('uuid is required')
		properties = {'uuid': uuid}
		properties.update(user_data)
		return self.protocol.update(credentials, properties)

	def getData(self, credentials, thing_uuid, **kwargs):
		return self.protocol.getData(credentials, thing_uuid, **kwargs)

	def postData(self, credentials, thing_uuid, user_data={}):
		properties = {'uuid': thing_uuid}
		properties.update(user_data)
		return self.protocol.postData(credentials, properties)

	def getThings(self, credentials, gateways=['*']):
		properties = {
			'gateways': gateways
		}
		return omitDevicesParameters(ProtoSocketio().getDevices(credentials, properties))

	def setData(self, credentials, thing_uuid, sensor_id, value):
		properties = {
			'uuid': thing_uuid,
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return ProtoSocketio().update(credentials, properties)

	def requestData(self, credentials, thing_uuid, sensor_id):
		properties = {
			'uuid': thing_uuid,
			'get_data': [{
				'sensor_id': sensor_id
				}]
		}
		return ProtoSocketio().update(credentials, properties)

	def setConfig(self, credentials, thing_uuid, sensor_id, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
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
		return ProtoSocketio().update(credentials, properties)
