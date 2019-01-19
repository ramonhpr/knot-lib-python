from uuid import UUID
import pytest
from knotpy.meshblu import Meshblu
from .credentials import credentials

credentials['port'] = 3001
KNOT_HTTP = Meshblu(protocol='http')
KNOT_SOCKET = Meshblu('socketio')
DEVICE_HTTP = None
DEVICE_SOCKET = None

def test_http_register():
    global DEVICE_HTTP
    DEVICE_HTTP = KNOT_HTTP.register_device(credentials, {'id': '111', 'test': 'http', 'schema': [
        {'sensor_id': 1, 'value_type': 2,
         'unit': 1, 'type_id': 13, 'name': 'Tank Volume'},
        {'sensor_id': 2, 'value_type':1,
         'unit': 1, 'type_id': 5, 'name': 'Outdoor Temperature'},
        {'sensor_id': 3, 'value_type':3,
         'unit': 0, 'type_id': 65521, 'name': 'Lamp Status'}]})

def test_socket_register():
    global DEVICE_SOCKET
    DEVICE_SOCKET = KNOT_SOCKET.register_device(credentials, {
        'id': '222', 'test': 'socketio',
        'schema': [
            {'sensor_id': 1, 'value_type': 2,
             'unit': 1, 'type_id': 13, 'name': 'Tank Volume'},
            {'sensor_id': 2, 'value_type':1,
             'unit': 1, 'type_id': 5, 'name': 'Outdoor Temperature'},
            {'sensor_id': 3, 'value_type':3,
             'unit': 0, 'type_id': 65521, 'name': 'Lamp Status'}]})

def test_http_is_dict():
    assert isinstance(DEVICE_HTTP, dict)
def test_socket_is_dict():
    assert isinstance(DEVICE_SOCKET, dict)

def test_http_has_valid_uuid():
    assert UUID(DEVICE_HTTP.get('uuid'), version=4)
def test_socket_has_valid_uuid():
    assert UUID(DEVICE_SOCKET.get('uuid'), version=4)

def test_http_property():
    assert DEVICE_HTTP.get('test') == 'http'
def test_socket_property():
    assert DEVICE_SOCKET.get('test') == 'socketio'

def test_http_empty_uuid():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(credentials)
        tmp['uuid'] = ''
        KNOT_HTTP.register_device(tmp)
def test_socket_empty_uuid():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(credentials)
        tmp['uuid'] = ''
        KNOT_SOCKET.register_device(tmp)

def test_http_empty_token():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(credentials)
        tmp['token'] = ''
        KNOT_HTTP.register_device(tmp)
def test_socket_empty_token():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(credentials)
        tmp['token'] = ''
        KNOT_SOCKET.register_device(tmp)

def test_http_invalid_credential():
    with pytest.raises(Exception):
        credentials['uuid'] = 'invalid'
        KNOT_HTTP.register_device(credentials)
def test_socket_invalid_credential():
    with pytest.raises(Exception):
        credentials['uuid'] = 'invalid'
        KNOT_SOCKET.register_device(credentials)
