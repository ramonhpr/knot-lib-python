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
	#TODO: setdata
	#TODO: getdata
	#TODO: setconfig