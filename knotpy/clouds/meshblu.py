import logging
import functools
from uuid import UUID
from knotpy.decorators import omit
from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
from .cloud import Cloud
__all__ = []

# Device parameters to be omitted
DEVICE_PARAMS = [
    '_id',
    'owner',
    'type',
    'ipAddress',
    'uuid',
    'token',
    'meshblu',
    'discoverWhitelist',
    'configureWhitelist',
    'socketid',
    'secure',
    'get_data',
    'schema',
    'set_data']

REGISTERED_PARAMS = list(DEVICE_PARAMS)
REGISTERED_PARAMS.remove('token') # don't omit token in register

def get_device_uuid(devices, device_id):
    try:
        device = [d for d in devices if d.get('id') == device_id][0]
    except IndexError:
        raise IndexError('Device not found')
    return device.get('uuid')

def can_convert_to_uuid(func):
    '''
        This decorator verify if it should use parent connection
        to convert the device id to uuid
    '''
    @functools.wraps(func)
    def decorator_use_uuid(self, credentials, device_id, *args, **kwargs):
        if self.use_parent_conn:
            devices = ProtoSocketio().get_devices(credentials, {'gateways': ['*']})
            uuid = get_device_uuid(devices, device_id)
            return func(self, credentials, uuid, *args, **kwargs)
        return func(self, credentials, device_id, *args, **kwargs)
    return decorator_use_uuid

def auth_http_headers(credentials):
    return {
        'meshblu_auth_uuid': credentials.get('uuid'),
        'meshblu_auth_token': credentials.get('token')
    }

def handle_response_error(res):
    if isinstance(res, dict):
        if res.get('error'):
            if isinstance(res.get('error'), dict):
                raise Exception(res.get('error').get('message'))
            elif isinstance(res, dict) and res.get('Error'):
                raise Exception(res.get('Error'))
            else:
                raise Exception(res.get('error'))
        elif res.get('code') == 404 or res.get('code') == 401:
            raise Exception(res.get('message'))
        else:
            return res
    else:
        return res

class Meshblu(Cloud):
    use_parent_conn = False
    def __init__(self, protocol, use_parent_conn=False):
        logging.info('Using protocol %s', protocol)
        self.use_parent_conn = use_parent_conn
        if self.use_parent_conn:
            logging.info('Requests will change id to uuid')
        self.protocol = {
            'socketio': ProtoSocketio,
            'http': lambda: ProtoHttp(
                headers=auth_http_headers,
                add_dev=lambda: {'type': 'POST', 'endpoint':'/devices'},
                list_dev=lambda: {'type': 'GET', 'endpoint':'/my_devices'},
                rm_dev=lambda uuid: {'type': 'DELETE', 'endpoint':'/devices/%s' %uuid},
                update_dev=lambda uuid: {'type': 'PUT', 'endpoint':'/devices/%s' %uuid},
                add_data=lambda uuid: {'type': 'POST', 'endpoint': '/data/%s' %uuid},
                list_data=lambda uuid: {'type': 'GET', 'endpoint': '/data/%s' %uuid},
                subs=lambda uuid: {'type': 'GET', 'endpoint': '/subscribe/%s' %uuid})
        }.get(protocol.lower())()

    @omit(REGISTERED_PARAMS)
    @can_convert_to_uuid
    def register_device(self, credentials, user_data=None):
        properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
        properties.update(user_data)
        try: # validate if uuid is in the right format
            UUID(credentials.get('uuid'), version=4)
        except ValueError as err:
            raise ValueError('Invalid credentials: ' + str(err))
        return self.protocol.register_device(credentials, properties)

    @omit(DEVICE_PARAMS)
    @can_convert_to_uuid
    def unregister_device(self, credentials, device_id, user_data=None):
        return handle_response_error(
            self.protocol.unregister_device(credentials, device_id, user_data)
        )

    @omit(DEVICE_PARAMS)
    def my_devices(self, credentials):
        return handle_response_error(self.protocol.my_devices(credentials)).get('devices')

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def subscribe(self, credentials, device_id, on_receive=None):
        self.protocol.subscribe(credentials, device_id, on_receive)

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def update(self, credentials, device_id, user_data=None):
        return handle_response_error(self.protocol.update(credentials, device_id, user_data))

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def get_data(self, credentials, device_id, **kwargs):
        return self.protocol.get_data(credentials, device_id, **kwargs)

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def post_data(self, credentials, device_id, user_data=None):
        properties = {'uuid': device_id}
        properties.update(user_data)
        return self.protocol.post_data(credentials, device_id, user_data)

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def list_sensors(self, credentials, device_id):
        devices = ProtoSocketio().get_devices(credentials, {'gateways': ['*']})
        try:
            device = [dev for dev in devices if dev.get('uuid') == device_id][0]
            return [sensor.get('sensor_id') for sensor in device['schema']]
        except KeyError:
            return []

    @classmethod
    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def get_sensor_details(cls, credentials, device_id, sensor_id):
        devices = ProtoSocketio().get_devices(credentials, {'gateways': ['*']})
        try:
            device = [dev for dev in devices if dev.get('uuid') == device_id][0]
            return [i for i in device['schema'] if i.get('sensor_id') == sensor_id][0]
        except KeyError:
            raise Exception('None sensor is registered in this thing')
        except IndexError:
            raise Exception('This thing has not this sensor_id %s' %sensor_id)

    @omit(DEVICE_PARAMS)
    def get_things(self, credentials, gateways=None):
        logging.warning('This function is using protocol socketio')
        properties = {
            'gateways': gateways or ['*']
        }
        return handle_response_error(ProtoSocketio().get_devices(credentials, properties))

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def set_data(self, credentials, device_id, sensor_id, value):
        properties = {
            'set_data': [{
                'sensor_id': sensor_id,
                'value': value
                }]
        }
        return handle_response_error(ProtoSocketio().update(credentials, device_id, properties))

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def request_data(self, credentials, device_id, sensor_id):
        properties = {
            'get_data': [{
                'sensor_id': sensor_id
                }]
        }
        return handle_response_error(ProtoSocketio().update(credentials, device_id, properties))

    @can_convert_to_uuid
    @omit(DEVICE_PARAMS)
    def send_config(self, credentials, device_id, sensor_id, event_flags, **kwargs):
        time_sec = kwargs.get('time_sec')
        lower_limit = kwargs.get('lower_limit')
        upper_limit = kwargs.get('upper_limit')
        properties = {
            'config': [{
                'sensor_id': sensor_id,
                'event_flags': event_flags,
                'time_sec': time_sec,
                'lower_limit': lower_limit,
                'upper_limit': upper_limit
                }]
        }
        return handle_response_error(ProtoSocketio().update(credentials, device_id, properties))
