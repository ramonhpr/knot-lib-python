import proto_socketio
import proto_http

class KnotProtocol(object):
	def __init__(self, protocol):
		self.protocol = {
			'socketio': proto_socketio.ProtoSocketio(),
			'http': proto_http.ProtoHttp()
		}.get(protocol)

	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		return self.protocol.registerDevice(credentials, properties)

	def unregisterDevice(self, credentials,user_data={}):
		return self.protocol.unregisterDevice(credentials, user_data)

	def myDevices(self, credentials):
		return self.protocol.myDevices(credentials)

	def getDevices(self, credentials):
		return self.protocol.getDevices(credentials)

	def subscribe(self, credentials, uuid, onReceive=None):
		self.protocol.subscribe(credentials, uuid, onReceive)

	def update(self, credentials, user_data={}):
		return self.protocol.update(credentials, user_data)

	def readData(self, credentials, thing_uuid, user_data={}):
		return proto_http.ProtoHttp().readData(credentials, thing_uuid, user_data)

	def postData(self, credentials, thing_uuid, user_data={}):
		properties = {'uuid': thing_uuid}
		properties.update(user_data)
		return self.protocol.postData(credentials, properties)

	def setData(self, credentials, thing_uuid, sensor_id, value):
		properties = {
			'uuid': thing_uuid,
			'set_data': [{
				'sensor_id': sensor_id,
				'value': value
				}]
		}
		return proto_socketio.ProtoSocketio().update(credentials, properties)

	def getData(self, credentials, thing_uuid, sensor_id):
		properties = {
			'uuid': thing_uuid,
			'get_data': [{
				'sensor_id': sensor_id
				}]
		}
		return proto_socketio.ProtoSocketio().update(credentials, properties)

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
		return proto_socketio.ProtoSocketio().update(credentials, properties)