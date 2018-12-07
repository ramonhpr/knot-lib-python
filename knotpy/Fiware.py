import logging
from .evt_flag import FLAG_CHANGE
from .proto_http import ProtoHttp
from .Cloud import Cloud
from .handler import handle_fiware_response
__all__ = []

def _omit(json, arr):
    return {k: v for k, v in json.items() if k not in arr}

def omit_device_parameters(device):
    return _omit(
        device, [
            'type',
            'isPattern',
            'attributes',
            'send_config_status',
            'send_config',
            'setProperties_status',
            'send_config_info',
            'setProperties',
            'setProperties_info'
        ])

def parse_attributes(attributes):
    attr_parsed = {}
    for attr in attributes:
        if attr.get('type') == 'number':
            attr_parsed[attr.get('name')] = float(attr.get('value'))
        elif attr.get('type') == 'boolean':
            attr_parsed[attr.get('name')] = bool(attr.get('value'))
        else:
            attr_parsed[attr.get('name')] = attr.get('value')
    return attr_parsed

def omit_devices_parameters(devices):
    for i, dev in enumerate(devices):
        dev = dev.get('contextElement')
        dev.update(parse_attributes(dev.get('attributes')))
        devices[i] = omit_device_parameters(dev)

    return devices

def auth_http_headers(credentials):
    return {
        'fiware-service': "knot",
        'fiware-servicepath': "/device/%s" %credentials.get('id') if credentials.get('id') else '/device',
    }

class Fiware(Cloud):
    def __init__(self, protocol):
        logging.info('Using protocol %s', protocol)
        self.iotagent_port = 4041
        self.protocol = {
            'http': ProtoHttp(
                headers=auth_http_headers,
                addDev=lambda: {'type': 'POST', 'endpoint':'/v2/entities'},
                listDev=lambda: {'type': 'POST', 'endpoint':'/v1/queryContext'},
                rmDev=lambda device_id: {'type': 'DELETE', 'endpoint':'/v2/entities/%s' %device_id},
                updateDev=lambda device_id: {'type': 'POST', 'endpoint':'/v1/updateContext'},
                addData=lambda device_id: {'type': 'POST', 'endpoint': '/data/%s' %device_id},
                listData=lambda device_id: {'type': 'GET', 'endpoint': '/v2/entities/%s?options=keyValues' %device_id},
                subs=lambda: {'type': 'POST', 'endpoint': 'v2/subscriptions'})
        }.get(protocol.lower())

    def register_device(self, credentials, user_data=None):
        logging.error('Missing implementation')

    def unregister_device(self, credentials, device_id, user_data=None):
        orion_response = self.protocol.unregister_device(credentials, device_id, user_data)
        try:
            return handle_fiware_response(orion_response)
        except Exception as err:
            raise err

        tmp_protocol = self.protocol
        tmp_protocol.rmDev = lambda device: {'type': 'DELETE', 'endpoint': '/iot/devices/%s' %device}
        iotagent_response = tmp_protocol.unregister_device({'servername': credentials['servername'], 'port': 4041}, device_id)
        try:
            return handle_fiware_response(iotagent_response)
        except Exception as err:
            raise err

    def update(self, credentials, device_id, user_data=None):
        body = {
            "contextElements": [
                {
                    "type": "device",
                    "isPattern": "false",
                    "id": device_id,
                    "attributes": [
                        {
                            "name": "setProperties",
                            "type": "command",
                            "value": user_data
                        }
                    ]
                }
            ],
            "updateAction": "UPDATE"
        }
        response = self.protocol.update(credentials, device_id, body).get('contextResponses')
        return handle_fiware_response(response)

    def list_sensors(self, credentials, device_id):
        body = {
            "entities": [
                {
                    "type": "sensor",
                    "isPattern": "true",
                    "id": "/*"
                }
            ]
        }
        credentials['id'] = device_id
        response = self.protocol.my_devices(credentials, body)
        try:
            if response.get('contextResponses'):
                devices = omit_devices_parameters(response.get('contextResponses'))
                return [{'id': sensor.get('id'), 'name': sensor.get('name')} for sensor in devices]
            return handle_fiware_response(response)
        except KeyError:
            return []
        except Exception as err:
            raise err



    def get_sensor_details(self, credentials, device_id, sensor_id):
        body = {
            "entities": [
                {
                    "type": "sensor",
                    "isPattern": "true",
                    "id": str(sensor_id)
                }
            ]
        }
        credentials['id'] = device_id
        response = self.protocol.my_devices(credentials, body)
        try:
            if response.get('contextResponses'):
                devices = omit_devices_parameters(response.get('contextResponses'))
                return [sensor for sensor in devices]
            return handle_fiware_response(response)
        except KeyError:
            return []
        except Exception as err:
            raise err


    def get_things(self, credentials, gateways=None):
        body = {
            'entities': [
                {
                    'type': 'device',
                    'isPattern': 'true',
                    'id': '/*'
                }
            ]
        }
        response = self.protocol.my_devices(credentials, body).get('contextResponses')
        if response:
            return omit_devices_parameters(response)
        raise Exception('Devices not found')

    def my_devices(self, credentials):
        return self.get_things(credentials)

    def request_data(self, credentials, device_id, sensor_id):
        body = {
            "contextElements": [
                {
                    "type": "sensor",
                    "isPattern": "false",
                    "id": sensor_id,
                    "attributes": [
                        {
                            "name": "get_data",
                            "type": "command",
                            "value": ""
                        }
                    ]
                }
            ],
            "updateAction": "UPDATE"
        }
        credentials['id'] = device_id
        response = self.protocol.update(credentials, device_id, body).get('contextResponses')
        return handle_fiware_response(response)

    def send_config(self, credentials, device_id, sensor_id, event_flags=FLAG_CHANGE, **kwargs):
        logging.error('Missing implementation')
        time_sec = kwargs.get('time_sec')
        lower_limit = kwargs.get('lower_limit')
        upper_limit = kwargs.get('upper_limit')
        body = {
            "contextElements": [
                {
                    "type": "device",
                    "isPattern": "false",
                    "id": sensor_id,
                    "attributes": [
                        {
                            "name": "send_config",
                            "type": "command",
                            "value": {
                                "sensor_id": sensor_id,
                                "event_flags": event_flags,
                                "time_sec": time_sec,
                                "lower_limit": lower_limit,
                                "upper_limit": upper_limit
                            }
                        }
                    ]
                }
            ],
            "updateAction": "UPDATE"
        }
        credentials['id'] = device_id
        response = self.protocol.update(credentials, device_id, body).get('contextResponses')
        return handle_fiware_response(response)

    def get_data(self, credentials, device_id, **kwargs):
        logging.error('Missing implementation')

    def subscribe(self, credentials, device_id, on_receive=None):
        logging.error('Missing implementation')

    def post_data(self, credentials, device_id, user_data=None):
        logging.error('Missing implementation')

    def set_data(self, credentials, device_id, sensor_id, value):
        body = {
            "contextElements": [
                {
                    "type": "sensor",
                    "isPattern": "false",
                    "id": sensor_id,
                    "attributes": [
                        {
                            "name": "set_data",
                            "type": "command",
                            "value": value
                        }
                    ]
                }
            ],
            "updateAction": "UPDATE"
        }
        credentials['id'] = device_id
        response = self.protocol.update(credentials, device_id, body).get('contextResponses')
        return handle_fiware_response(response)
