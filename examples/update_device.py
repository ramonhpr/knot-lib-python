from knotpy import *
from credentials import *

knot = KnotConnection(credentials)

try:
    thing_uuid = 'b4db3ef2-b969-4a49-aba1-1577d40f0000'
    knot.update(thing_uuid, {'test': 'change'})
except Exception as err:
    print('[Err]'+str(err))
