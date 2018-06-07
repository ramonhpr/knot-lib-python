from socketIO_client import SocketIO, BaseNamespace
import logging
__all__=[]

class KNoTNamespace(BaseNamespace):
	def on_connect(self, *args):
		logging.info('Connected')

	def on_devices(self, *args):
		logging.info('Get things')
		logging.info(args[0])
		ProtoSocketio.result = args[0]
		self.disconnect()

	def on_unregister(self, *args):
		logging.info('Unregister')
		result = args[0]
		logging.info(result)
		if result.get('error'):
			raise Exception(result['error'])
		self.disconnect()

	def on_subscribe(self, *args):
		logging.info('subscribe')
		result = args[0]
		logging.info(args[0])
		if result.get('error'):
			raise Exception(result['error']['error']['message'])

	def on_config(self, *args):
		logging.info('config')
		logging.info(args[0])
		if ProtoSocketio.methodCallBack:
			ProtoSocketio().methodCallBack(args[0])
	def on_error(self, *args):
		logging.info('error')
		logging.info(args)

	def on_register(self, *args):
		logging.info('Registered')
		logging.info(args[0])
		ProtoSocketio.result = args[0]
		self.disconnect()

	def on_mydevices(self, *args):
		logging.info('MyDevices')
		logging.info(args[0])
		ProtoSocketio.result = args[0]
		self.disconnect()

	def on_update(self, *args):
		logging.info('Update')
		logging.info(args[0])
		ProtoSocketio.result = args[0]
		self.disconnect()

	def on_data(self, *args):
		logging.info('Post Data')
		logging.info(args)
		ProtoSocketio.result = args[0] if args else None
		self.disconnect()

	def on_getdata(self, *args):
		logging.info('Get data')
		logging.info(args[0])
		ProtoSocketio.result = args[0]
		self.disconnect()

	def on_ready(self, *args):
		logging.info('Ready')
		logging.info(args)
		# The below 'switch' select which callback must be emitted
		emit = {
			'getDevices': lambda: self.emit('devices', ProtoSocketio.methodArgs, self.on_devices),
			'registerDevice': lambda: self.emit('register', ProtoSocketio.methodArgs, self.on_register),
			'myDevices': lambda: self.emit('mydevices', { }, self.on_mydevices),
			'subscribe': lambda: self.emit('subscribe', ProtoSocketio.methodArgs, self.on_subscribe),
			'update': lambda: self.emit('update', ProtoSocketio.methodArgs, self.on_update),
			'unregister': lambda: self.emit('unregister', ProtoSocketio.methodArgs, self.on_unregister),
			'data': lambda : self.emit('data', ProtoSocketio.methodArgs, self.on_data),
			'getdata': lambda : self.emit('getdata', ProtoSocketio.methodArgs, self.on_getdata)
		}.get(ProtoSocketio.methodName)
		logging.info('Emitting signal for ' + ProtoSocketio.methodName)
		emit()

	def on_notReady(self, *args):
		logging.info('notReady')
		logging.info(args)
		raise Exception('Invalid credentials')

	def on_identify(self, *args):
		logging.info('Identify')
		logging.info(args)
		self.emit('identity', ProtoSocketio.cred)

class ProtoSocketio(object):
	methodName = None
	methodArgs = {}
	methodCallBack = None
	cred = {}
	result = {}

	def __signinEmit(self, credentials, signalToEmit, properties={}, callback=None):
		ProtoSocketio.cred = {'uuid': credentials.get('uuid'), 'token': credentials.get('token')}
		ProtoSocketio.methodName = signalToEmit
		ProtoSocketio.methodArgs = properties
		ProtoSocketio.methodCallBack = callback
		ProtoSocketio.result = {}
		try:
			with SocketIO(credentials.get('servername'), credentials.get('port'), KNoTNamespace, wait_for_connection=False) as socketIO:
				socketIO.wait()
		except AttributeError as err:
			raise AttributeError('Connection not established, verify servername and port')
		return ProtoSocketio.result

	def myDevices(self, credentials):
		return self.__signinEmit(credentials, 'myDevices')

	def getDevices(self, credentials, properties={}):
		return self.__signinEmit(credentials, 'getDevices', properties)

	def registerDevice(self, credentials, properties={}):
		return self.__signinEmit(credentials, 'registerDevice', properties)

	def unregisterDevice(self, credentials, properties={}):
		return self.__signinEmit(credentials, 'unregister', properties)

	def subscribe(self, credentials, uuid, user_callback):
		return self.__signinEmit(credentials, 'subscribe', {'uuid': uuid}, lambda socket, result: user_callback(result))

	def update(self, credentials, properties={}):
		return self.__signinEmit(credentials, 'update', properties)

	def postData(self, credentials, user_data={}):
		return self.__signinEmit(credentials, 'data', user_data)

	def readData(self, credentials, uuid, **kwargs):
		kwargs.update({
			'uuid': credentials.get('uuid'),
			'token': credentials.get('token'),
			'target': uuid,
			'limit': kwargs.get('limit'),
			'start': kwargs.get('start'),
			'stop': kwargs.get('stop')
		})
		return self.__signinEmit(credentials, 'getdata', kwargs)
