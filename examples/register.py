from knotpy import *
credentials = {
	'uuid': '533703c2-b60c-45c9-bc6b-1f7301ba0000',
	'token': '6ab7f76b86d1cf6a29f40ff1a1b053dec3e9d24c',
	'servername': 'localhost',
	'port': 3000
}

knot = KnotConnection('http',credentials)
try:
    device = knot.registerDevice()
    print(device.get('uuid'))
    print(device.get('token'))
except Exception as err:
	print('[ERR]: '+str(err))
