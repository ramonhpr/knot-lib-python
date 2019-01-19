import pytest
from knotpy import KnotConnection
from .credentials import credentials

KNOT_HTTP = KnotConnection(credentials, protocol='http')
KNOT_SOCKETIO = KnotConnection(credentials, protocol='socketio')
MY_DEVICES_HTTP = None
MY_DEVICES_SOCKET = None

def test_http_my_devices():
    global MY_DEVICES_HTTP
    MY_DEVICES_HTTP = KNOT_HTTP.get_devices()
def test_socket_my_devices():
    global MY_DEVICES_SOCKET
    MY_DEVICES_SOCKET = KNOT_SOCKETIO.get_devices()

def test_http_is_list():
    assert isinstance(MY_DEVICES_HTTP, list)
def test_socket_is_dict():
    assert isinstance(MY_DEVICES_SOCKET, list)

# def test_http_empty_uuid(): # FIXME: it breaks the cloud
#     with pytest.raises(Exception):
#         from copy import deepcopy
#         tmp = deepcopy(KNOT_HTTP)
#         tmp.credentials['uuid'] = ''
#         tmp.get_devices()
# def test_socket_empty_uuid():
#     with pytest.raises(Exception):
#         from copy import deepcopy
#         tmp = deepcopy(KNOT_SOCKETIO)
#         tmp.credentials['uuid'] = ''
#         return tmp.get_devices()

def test_http_empty_token():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(KNOT_HTTP)
        tmp.credentials['token'] = ''
        tmp.get_devices()
def test_socket_empty_token():
    with pytest.raises(Exception):
        from copy import deepcopy
        tmp = deepcopy(KNOT_HTTP)
        tmp.credentials['token'] = ''
        tmp.get_devices()

def test_http_invalid_credential():
    with pytest.raises(Exception):
        KNOT_HTTP.credentials['uuid'] = 'invalid'
        KNOT_HTTP.get_devices()
def test_socket_invalid_credential():
    with pytest.raises(Exception):
        KNOT_SOCKETIO.credentials['uuid'] = 'invalid'
        KNOT_SOCKETIO.get_devices()
