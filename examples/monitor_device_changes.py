from knot import *
credentials = {
	'uuid': '533703c2-b60c-45c9-bc6b-1f7301ba0000',
	'token': '6ab7f76b86d1cf6a29f40ff1a1b053dec3e9d24c',
	'servername': 'localhost',
	'port': 3000
}

knot = KnotConnection('socketio', credentials)
def onDeviceChange(device):
    print(device)
try:
    thing_uuid = 'b4db3ef2-b969-4a49-aba1-1577d40f0000'
    knot.subscribe(thing_uuid, onDeviceChange)
except Exception as err:
    print('[Err]'+str(err))