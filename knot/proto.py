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

	def update(self, credentials, properties={}):
		return self.protocol.update(credentials, properties)

	def readData(self, credentials, thing_uuid, properties={}):
		return proto_http.ProtoHttp().readData(credentials, thing_uuid, properties)

	def postData(self, credentials, thing_uuid, properties={}):
		return proto_http.ProtoHttp().postData(credentials, thing_uuid, properties)