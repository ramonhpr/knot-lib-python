import logging
from socketIO_client import SocketIO, BaseNamespace
from .proto import Protocol
__all__ = []

class KNoTNamespace(BaseNamespace):
    def on_connect(self):
        logging.info('Connected')

    def on_devices(self, *args):
        logging.info('Get things')
        logging.info(args[0])
        ProtoSocketio.result = args[0]
        self.disconnect()

    def on_unreg(self, *args):
        logging.info('Unregister')
        result = args[0]
        logging.info(result)
        if result.get('error'):
            raise Exception(result['error'])
        self.disconnect()

    @classmethod
    def on_subs(cls, *args):
        logging.info('subscribe')
        result = args[0]
        logging.info(args[0])
        if result.get('error'):
            raise Exception(result['error']['error']['message'])

    def on_config(self, *args):
        logging.info('config')
        logging.info(args[0])
        if ProtoSocketio.method_cb is not None:
            ProtoSocketio.method_cb(args[0]) #pylint: disable=not-callable
        else:
            self.disconnect()
    def on_error(self, data):
        logging.info('error')
        logging.info(data)

    def on_register(self, *args):
        logging.info('Registered')
        logging.info(args[0])
        ProtoSocketio.result = args[0]
        self.disconnect()

    def on_my_devices(self, *args):
        logging.info('my_devices')
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

    def on_get_data(self, *args):
        logging.info('Get data')
        logging.info(args[0])
        ProtoSocketio.result = args[0]
        self.disconnect()

    def on_ready(self, *args):
        logging.info('Ready')
        logging.info(args)
        # The below 'switch' select which callback must be emitted
        emit = {
            'devices': lambda: self.emit('devices', ProtoSocketio.method_args, self.on_devices),
            'register': lambda: self.emit('register', ProtoSocketio.method_args, self.on_register),
            'my_devices': lambda: self.emit('my_devices', {}, self.on_my_devices),
            'subscribe': lambda: self.emit('subscribe', ProtoSocketio.method_args, self.on_subs),
            'update': lambda: self.emit('update', ProtoSocketio.method_args, self.on_update),
            'unregister': lambda: self.emit('unregister', ProtoSocketio.method_args, self.on_unreg),
            'data': lambda: self.emit('data', ProtoSocketio.method_args, self.on_data),
            'getdata': lambda: self.emit('getdata', ProtoSocketio.method_args, self.on_get_data)
        }.get(ProtoSocketio.method_name)
        logging.info('Emitting signal for %s', ProtoSocketio.method_name)
        emit()

    def on_notReady(self, *args): #pylint: disable=invalid-name
        logging.info('notReady')
        logging.info(args)
        self.disconnect()
        raise Exception('Invalid credentials')

    def on_identify(self, *args):
        logging.info('Identify')
        logging.info(args)
        self.emit('identity', ProtoSocketio.cred)

class ProtoSocketio(Protocol):
    method_name = None
    method_args = {}
    method_cb = None
    cred = {}
    result = {}

    @classmethod
    def __signin_emit(cls, credentials, signal_to_emit, properties=None, callback=None):
        ProtoSocketio.cred = {'uuid': credentials.get('uuid'), 'token': credentials.get('token')}
        ProtoSocketio.method_name = signal_to_emit
        ProtoSocketio.method_args = properties
        ProtoSocketio.method_cb = callback
        ProtoSocketio.result = {}
        try:
            with SocketIO(credentials.get('servername'),
                          credentials.get('port'),
                          KNoTNamespace,
                          wait_for_connection=False) as socket_io:
                socket_io.wait()
        except AttributeError as err:
            raise AttributeError('Connection not established, verify servername and port\n%s' %err)
        except KeyboardInterrupt:
            pass
        return ProtoSocketio.result

    def my_devices(self, credentials, user_data=None):
        return self.__signin_emit(credentials, 'my_devices')

    def get_devices(self, credentials, user_data=None):
        return self.__signin_emit(credentials, 'devices', user_data)

    def register_device(self, credentials, user_data=None):
        return self.__signin_emit(credentials, 'register', user_data)

    def unregister_device(self, device_id, credentials, properties=None):
        return self.__signin_emit(credentials, 'unregister', properties)

    def subscribe(self, credentials, device_id, on_receive=None):
        return self.__signin_emit(credentials, 'subscribe',
                                  {'uuid': device_id}, lambda socket, result: on_receive(result))

    def update(self, credentials, device_id, user_data=None):
        user_data.update({'uuid':device_id})
        return self.__signin_emit(credentials, 'update', user_data)

    def post_data(self, credentials, device_id, user_data=None):
        return self.__signin_emit(credentials, 'data', user_data)

    def get_data(self, credentials, device_id, **kwargs):
        kwargs.update({
            'uuid': credentials.get('uuid'),
            'token': credentials.get('token'),
            'target': device_id,
            'limit': kwargs.get('limit'),
            'start': kwargs.get('start'),
            'finish': kwargs.get('finish')
        })
        return self.__signin_emit(credentials, 'getdata', kwargs)
