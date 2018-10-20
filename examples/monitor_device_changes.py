from knotpy import *
from credentials import *

knot = KnotConnection(credentials)
def onDeviceChange(device):
    print(device)
try:
    thing_uuid = '113'
    knot.subscribe(thing_uuid, onDeviceChange)
except Exception as err:
    print('[Err]'+str(err))
