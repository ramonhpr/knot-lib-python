import pytest
from knotpy import KnotConnection
from .credentials import credentials
# TODO: Put validation package

KNOT_HTTP = KnotConnection(credentials, protocol='http')
KNOT_SOCKETIO = KnotConnection(credentials, protocol='socketio')
DATA_HTTP = None
DATA_SOCKETIO = None

def test_http_get_data():
    global DATA_HTTP
    DATA_HTTP = KNOT_HTTP.get_data('111')
def test_socket_get_data():
    global DATA_SOCKETIO
    DATA_SOCKETIO = KNOT_SOCKETIO.get_data('222')

def test_http_is_list():
    assert isinstance(DATA_HTTP, list)
def test_socket_is_list():
    assert isinstance(DATA_SOCKETIO, list)

def test_http_read_one_data():
    tmp = KNOT_HTTP.get_data('111', limit=1)
    assert len(tmp) <= 1
def test_socket_read_one_data():
    tmp = KNOT_SOCKETIO.get_data('222', limit=1)
    assert len(tmp) <= 1

# FIXME: should raise exception
def test_http_wrong_query():
    with pytest.raises(Exception):
        KNOT_HTTP.get_data('111', limit='lala', start=1)
def test_socket_wrong_query():
    with pytest.raises(Exception):
        KNOT_SOCKETIO.get_data('222', limit='lala', start=1)

def test_http_empty_uuid():
    with pytest.raises(Exception):
        KNOT_HTTP.get_data('')
def test_socket_empty_uuid(): # FIXME: Should raise exception
    with pytest.raises(Exception):
        KNOT_SOCKETIO.get_data('')

def test_http_invalid_credential(): # FIXME: Should raise exception
    with pytest.raises(Exception):
        KNOT_HTTP.get_data('invalid')
def test_socket_invalid_credential(): # FIXME: Should raise exception
    with pytest.raises(Exception):
        KNOT_SOCKETIO.get_data('invalid')
