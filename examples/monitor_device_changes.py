from knotpy import *
from credentials import *

knot = KnotConnection(credentials)
def on_device_change(device):
    print(device)
try:
    thing_uuid = '113'
    knot.subscribe(thing_uuid, on_device_change)
except Exception as err:
    print('[Err]'+str(err))
