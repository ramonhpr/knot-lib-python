from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
__all__=[]

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
		return self.protocol.myDevices(credentials)

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

	def readData(self, credentials, thing_uuid, **kwargs):
		return self.protocol.readData(credentials, thing_uuid, **kwargs)

	def postData(self, credentials, thing_uuid, user_data={}):
		properties = {'uuid': thing_uuid}
		properties.update(user_data)
		return self.protocol.postData(credentials, properties)

	def getThings(self, credentials, gateways=['*']):
		properties = {
			'gateways': gateways
		}
		return ProtoSocketio().getDevices(credentials, properties)

	def setData(self, credentials, thing_uuid, sensor_id, value):
		properties = {
			'uuid': thing_uuid,
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return ProtoSocketio().update(credentials, properties)

	def getData(self, credentials, thing_uuid, sensor_id):
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
