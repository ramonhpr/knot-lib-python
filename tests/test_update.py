import pytest
from knotpy import KnotConnection
from .credentials import credentials

KNOT_HTTP = KnotConnection(credentials, protocol='http')
KNOT_SOCKETIO = KnotConnection(credentials, protocol='socketio')
DATA_HTTP = None
DATA_SOCKETIO = None

def test_http_set_data():
    global DATA_HTTP
    DATA_HTTP = KNOT_HTTP.set_data('111', 1, True)
def test_socket_set_data():
    global DATA_SOCKETIO
    DATA_SOCKETIO = KNOT_SOCKETIO.set_data('222', 1, True)

def test_http_set_data_is_dict():
    assert isinstance(DATA_HTTP, dict)
def test_socket_set_data_is_dict():
    assert isinstance(DATA_SOCKETIO, dict)

def test_http_request_data():
    global DATA_HTTP
    DATA_HTTP = KNOT_HTTP.request_data('111', 1)
def test_socket_request_data():
    global DATA_SOCKETIO
    DATA_SOCKETIO = KNOT_SOCKETIO.request_data('222', 1)

def test_http_request_data_is_dict():
    assert isinstance(DATA_HTTP, dict)
def test_socket_request_data_is_dict():
    assert isinstance(DATA_SOCKETIO, dict)

def test_http_send_config():
    global DATA_HTTP
    DATA_HTTP = KNOT_HTTP.send_config('111', 1)
def test_socket_send_config():
    global DATA_SOCKETIO
    DATA_SOCKETIO = KNOT_SOCKETIO.send_config('222', 1)

def test_http_send_config_is_dict():
    assert isinstance(DATA_HTTP, dict)
def test_socket_send_config_is_dict():
    assert isinstance(DATA_SOCKETIO, dict)
