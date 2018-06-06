from knotpy import *
from credentials import *

knot = KnotConnection('socketio', credentials)
def onDeviceChange(device):
    print(device)
try:
    thing_uuid = 'b4db3ef2-b969-4a49-aba1-1577d40f0000'
    knot.subscribe(thing_uuid, onDeviceChange)
except Exception as err:
    print('[Err]'+str(err))