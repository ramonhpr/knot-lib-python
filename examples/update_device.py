from knotpy import *
from credentials import *

knot = KnotConnection(credentials, protocol='http')

try:
    thing_uuid = '113'
    knot.update(thing_uuid, {'test': 'change2'})
except Exception as err:
    print('[Err]'+str(err))
