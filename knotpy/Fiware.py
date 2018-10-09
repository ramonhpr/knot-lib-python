import logging
from uuid import UUID
from .proto_http import ProtoHttp
from .Cloud import Cloud
__all__=[]

def _omit(json, arr):
	return {k: v for k,v in json.items() if k not in arr}

def omitDeviceParameters(device):
	return _omit(device,['_id',
	'owner',
	'type',
	'ipAddress',
	'token',
	'meshblu',
	'discoverWhitelist',
	'configureWhitelist',
	'socketid',
	'secure',
	'get_data',
	'set_data'])

def omitDevicesParameters(devices):
	for i,dev in enumerate(devices):
		devices[i] = omitDeviceParameters(dev)
	return devices

def authHttpHeaders(credentials):
	return {
		'fiware-service': "knot",
		'fiware-servicepath': "/device/%s" %credentials.get('id') if device else '/device'
	}

def addDevice():
	return {'type': 'POST', 'endpoint':'/v2/entities'}

def rmDevice(device):
	return {'type': 'POST', 'endpoint':'/v2/entities/%s' %device}

def listDevice():
	return {'type': 'POST', 'endpoint':'/v1/queryContext'}

def updateDevice(uuid):
	return {'type': 'POST', 'endpoint':'/v1/updateContext'}

def listData(uuid):
	return {'type': 'POST', 'endpoint': '/data/%s' %uuid}

def addData(uuid):
	return {'type': 'POST', 'endpoint': '/data/%s' %uuid}

def subs(uuid):
	return {'type': 'POST', 'endpoint': '/subscribe/%s' %uuid}

class Fiware(Cloud):
	def __init__(self, protocol):
		logging.info('Using protocol ' + protocol)
		self.protocol = {
			'http': ProtoHttp(headers=authHttpHeaders,
							addDev=addDevice,
							rmDev=rmDevice,
							listDev=listDevice,
							updateDev=updateDevice,
							addData=addData,
							listData=listData,
							subs=subs)
		}.get(protocol.lower())

	def registerDevice(self, credentials, user_data={}):
		return self.protocol.registerDevice(credentials, user_data)
	
	def getThings(self, credentials, gateways=['*']):
		properties = {
			'entities': [
				{
					'type': 'device',
					'idPattern': 'true',
					'id': '/*'
				}
			]
		}
		return self.protocol.myDevices(credentials, properties)
		