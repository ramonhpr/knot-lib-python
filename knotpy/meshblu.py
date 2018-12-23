import logging
from uuid import UUID
from .evt_flag import FLAG_CHANGE
from .proto_socketio import ProtoSocketio
from .proto_http import ProtoHttp
from .handler import handle_response_error
from .cloud import Cloud
__all__ = []

def _omit(json, arr):
    return {k: v for k, v in json.items() if k not in arr}

def omit_device_params(device):
    return _omit(
        device, [
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
            'set_data'])

def omit_device_registered_params(device):
    return _omit(
        device, [
            '_id',
            'owner',
            'type',
            'ipAddress',
            'meshblu',
            'discoverWhitelist',
            'configureWhitelist',
            'socketid',
            'secure',
            'get_data',
            'set_data'])

def omit_devices_params(devices):
    for i, dev in enumerate(devices):
        devices[i] = omit_device_params(dev)
    return devices

def get_device_uuid(devices, device_id):
    try:
        device = [d for d in devices if d.get('id') == device_id][0]
    except IndexError:
        raise IndexError('Device not found')
    return device.get('uuid')

def auth_http_headers(credentials):
    return {
        'meshblu_auth_uuid': credentials.get('uuid'),
        'meshblu_auth_token': credentials.get('token')
    }

class Meshblu(Cloud):
    def __init__(self, protocol):
        logging.info('Using protocol %s', protocol)
        self.protocol = {
            'socketio': ProtoSocketio,
            'http': lambda: ProtoHttp(
                headers=auth_http_headers,
                addDev=lambda: {'type': 'POST', 'endpoint':'/devices'},
                listDev=lambda: {'type': 'GET', 'endpoint':'/my_devices'},
                rmDev=lambda uuid: {'type': 'DELETE', 'endpoint':'/devices/%s' %uuid},
                updateDev=lambda uuid: {'type': 'PUT', 'endpoint':'/devices/%s' %uuid},
                addData=lambda uuid: {'type': 'POST', 'endpoint': '/data/%s' %uuid},
                listData=lambda uuid: {'type': 'GET', 'endpoint': '/data/%s' %uuid},
                subs=lambda uuid: {'type': 'GET', 'endpoint': '/subscribe/%s' %uuid})
        }.get(protocol.lower())()

    def register_device(self, credentials, user_data=None):
        properties = {'type':'KNoTDevice', 'owner': credentials['uuid']}
        properties.update(user_data)
        try: # validate if uuid is in the right format
            UUID(credentials.get('uuid'), version=4)
        except ValueError as err:
            raise ValueError('Invalid credentials: ' + str(err))
        return omit_device_registered_params(self.protocol.register_device(credentials, properties))

    def unregister_device(self, credentials, device_id, user_data=None):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        return omit_device_params(handle_response_error(self.protocol.unregister_device(credentials, uuid, user_data)))

    def my_devices(self, credentials):
        return omit_devices_params(handle_response_error(self.protocol.my_devices(credentials)).get('devices'))

    def subscribe(self, credentials, device_id, on_receive=None):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        self.protocol.subscribe(credentials, uuid, on_receive)

    def update(self, credentials, device_id, user_data=None):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        properties = {'uuid': uuid}
        properties.update(user_data)
        return omit_device_params(handle_response_error(self.protocol.update(credentials, uuid, properties)))

    def get_data(self, credentials, device_id, **kwargs):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        return self.protocol.get_data(credentials, uuid, **kwargs)

    def post_data(self, credentials, device_id, user_data=None):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        properties = {'uuid': uuid}
        properties.update(user_data)
        return self.protocol.post_data(credentials, uuid, properties)

    def list_sensors(self, credentials, device_id):
        devices = ProtoSocketio().getDevices(credentials, {'gateways': ['*']})
        uuid = get_device_uuid(devices, device_id)
        try:
            device = [dev for dev in devices if dev.get('uuid') == uuid][0]
            return [sensor.get('sensor_id') for sensor in device['schema']]
        except KeyError:
            return []

    @classmethod
    def get_sensor_details(cls, credentials, device_id, sensor_id):
        devices = ProtoSocketio().getDevices(credentials, {'gateways': ['*']})
        uuid = get_device_uuid(devices, device_id)
        try:
            device = [dev for dev in devices if dev.get('uuid') == uuid][0]
            return [i for i in device['schema'] if i.get('sensor_id') == sensor_id][0]
        except KeyError:
            raise Exception('None sensor is registered in this thing')
        except IndexError:
            raise Exception('This thing has not this sensor_id %s' %sensor_id)

    def get_things(self, credentials, gateways=None):
        logging.warning('This function is using protocol socketio')
        properties = {
            'gateways': gateways or ['*']
        }
        return omit_devices_params(handle_response_error(ProtoSocketio().getDevices(credentials, properties)))

    def set_data(self, credentials, device_id, sensor_id, value):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        properties = {
            'set_data': [{
                'sensor_id': sensor_id,
                'value': value
                }]
        }
        return omit_device_params(handle_response_error(ProtoSocketio().update(credentials, uuid, properties)))

    def request_data(self, credentials, device_id, sensor_id):
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        properties = {
            'get_data': [{
                'sensor_id': sensor_id
                }]
        }
        return omit_device_params(handle_response_error(ProtoSocketio().update(credentials, uuid, properties)))

    def send_config(self, credentials, device_id, sensor_id, event_flags=FLAG_CHANGE, **kwargs):
        time_sec = kwargs.get('time_sec')
        lower_limit = kwargs.get('lower_limit')
        upper_limit = kwargs.get('upper_limit')
        uuid = get_device_uuid(
            ProtoSocketio().getDevices(credentials, {'gateways': ['*']}),
            device_id)
        properties = {
            'config': [{
                'sensor_id': sensor_id,
                'event_flags': event_flags,
                'time_sec': time_sec,
                'lower_limit': lower_limit,
                'upper_limit': upper_limit
                }]
        }
        return omit_device_params(handle_response_error(ProtoSocketio().update(credentials, uuid, properties)))
