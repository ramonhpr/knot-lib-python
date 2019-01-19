import pytest
from knotpy import KnotConnection
from .credentials import credentials

KNOT_HTTP = KnotConnection(credentials, protocol='http')
KNOT_SOCKETIO = KnotConnection(credentials, protocol='socketio')
SENSORS_HTTP, DETAILS_HTTP = None, []
SENSORS_SOCKETIO, DETAILS_SOCKETIO = None, []

def test_http_list_sensors():
    global SENSORS_HTTP
    SENSORS_HTTP = KNOT_HTTP.list_sensors('111')
def test_socket_list_sensors():
    global SENSORS_SOCKETIO
    SENSORS_SOCKETIO = KNOT_SOCKETIO.list_sensors('222')

def test_http_is_list():
    assert isinstance(SENSORS_HTTP, list)
def test_socket_is_list():
    assert isinstance(SENSORS_SOCKETIO, list)

def test_http_get_sensors_details():
    for sensor in SENSORS_HTTP:
        DETAILS_HTTP.append(KNOT_HTTP.get_sensor_details('111', sensor))
def test_socket_get_sensors_details():
    for sensor in SENSORS_SOCKETIO:
        DETAILS_SOCKETIO.append(KNOT_SOCKETIO.get_sensor_details('222', sensor))

def test_http_details_is_dict():
    for sensor in DETAILS_HTTP:
        assert isinstance(sensor, dict)
def test_socket_details_is_dict():
    for sensor in DETAILS_SOCKETIO:
        assert isinstance(sensor, dict)
