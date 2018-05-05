import proto_socketio

class KnotProtocol(object):
	def __init__(self, protocol):
		self.protocol = {
			'socketio': proto_socketio.ProtoSocketio()
		}.get(protocol)

	def registerDevice(self, credentials, user_data={}):
		properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
		properties.update(user_data)
		return self.protocol.registerDevice(credentials, properties)

	
	def myDevices(self, credentials):
		return self.protocol.myDevices(credentials)

	def getDevices(self, credentials):
		return self.protocol.getDevices(credentials)
