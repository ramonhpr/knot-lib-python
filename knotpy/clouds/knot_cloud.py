import logging
import functools
from .client_ws import ClientWs
from .cloud import Cloud

def _is_ready(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
        if self.ready:
            func(self, *args, **kwargs)
        else:
            raise Exception('Not ready')
    return func_wrapper

class KnotCloud(Cloud):
    def __init__(self, protocol, credentials):
        logging.info('Using protocol %s', protocol)
        self.client = {
            'ws': ClientWs
        }.get(protocol.lower())('ws.test', 443)
        self.result = {}
        self.ready = False
        self._send_identity(credentials)

    def _send_identity(self, credentials):
        def on_ready(_data):
            self.ready = True
        self.client.send_frame('identity', credentials)
        self.client.once('ready', on_ready)

    def _on_result(self, result):
        self.result = result

    @_is_ready
    def register_device(self, user_data=None):
        self.client.send_frame('register', user_data)
        self.client.once('registered', self._on_result)
        return self.result

    @_is_ready
    def unregister_device(self, device_id, user_data=None):
        self.client.send_frame('unregister', {'id': device_id})
        self.client.once('unregistered', self._on_result)
        return self.result

    @_is_ready
    def my_devices(self):
        # TODO: implement query
        self.client.send_frame('devices', {})
        self.client.once('devices', self._on_result)
        return self.result

    @_is_ready
    def create_session_token(self, device_id):
        self.client.send_frame('token', {'id': device_id})
        self.client.once('created', self._on_result)
        return self.result

    @_is_ready
    def revoke_session_token(self, device_id, token):
        self.client.send_frame('revoke', {'id': device_id, 'token': token})
        self.client.once('revoked', self._on_result)
        return self.result

    @_is_ready
    def update_schema(self, schema):
        self.client.send_frame('schema', {'schema': schema})
        self.client.once('updated', self._on_result)
        return self.result

    @_is_ready
    def activate(self, device_id):
        self.client.send_frame('activate', {'id': device_id})
        self.client.once('activated', self._on_result)
        return self.result

    @_is_ready
    def update_metadata(self, device_id, metadata=None):
        metadata.update({'id': device_id})
        self.client.send_frame('metadata', metadata)
        self.client.once('updated', self._on_result)
        return self.result

    @_is_ready
    def publish_data(self, sensor_id, value):
        self.client.send_frame('data', {'sensorId': sensor_id, 'value': value})
        self.client.once('published', self._on_result)
        return self.result

    @_is_ready
    def get_data(self, device_id, sensor_ids):
        self.client.send_frame('getdata', {'id': device_id, 'sensorIds': sensor_ids})
        self.client.once('sent', self._on_result)
        return self.result

    @_is_ready
    def set_data(self, device_id, data):
        self.client.send_frame('setdata', {'id': device_id, 'data': data})
        self.client.once('sent', self._on_result)
        return self.result
