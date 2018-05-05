import proto_socketio

class KnotProtocol(object):
	def __init__(self, protocol):
		self.protocol = {
			'socketio': proto_socketio.ProtoSocketio()
		}.get(protocol)

	def getDevices(self, credentials):
		return self.protocol.getDevices(credentials)
