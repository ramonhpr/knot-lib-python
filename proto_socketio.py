from socketIO_client import SocketIO, BaseNamespace
import logging, sys, os
if os.environ.get('DEBUG'):
	logging.basicConfig(format='KNOT_DEBUG: %(message)s', stream=sys.stderr, level=logging.INFO)

class KNoTNamespace(BaseNamespace):
	def on_connect(self, *args):
		logging.info('Connected')

	def on_devices(self, *args):
		ProtoSocketio.result = args[0]
		self.close()

	def on_unregister(self, *args):
		logging.info(args)

	def on_config(self, *args):
		logging.info(args)

	def on_register(self, *args):
		logging.info('Registered')
		ProtoSocketio.result = args[0]
		self.close()

	def on_ready(self, *args):
		logging.info('Ready')
		# The below 'switch' select which callback must be emitted
		emit = {
			'getDevices': lambda: self.emit('devices', { 'gateways':['*'] }, self.on_devices),
			'registerDevice': lambda: self.emit('register', ProtoSocketio.methodArgs, self.on_register)
		}.get(ProtoSocketio.methodCall)
		logging.info('Emitting signal for ' + ProtoSocketio.methodCall)
		emit()

	def on_identify(self, *args):
		logging.info('Identify')
		self.emit('identity', ProtoSocketio.cred)

class ProtoSocketio(object):
	methodCall = None
	methodArgs = {}
	cred = {}
	result = {}

	def __signinEmit(self, credentials, signalToEmit, properties={}):
		ProtoSocketio.cred = credentials
		ProtoSocketio.methodCall = signalToEmit
		ProtoSocketio.methodArgs = properties
		with SocketIO(credentials['servername'], credentials['port'], KNoTNamespace) as socketIO:
			try:
				socketIO.wait()
			except Exception as err:
				pass
		return ProtoSocketio.result

	def getDevices(self, credentials):
		return self.__signinEmit(credentials, 'getDevices') 

	def registerDevice(self, credentials, properties={}):
		return self.__signinEmit(credentials, 'registerDevice', properties)

