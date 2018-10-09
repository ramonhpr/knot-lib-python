import logging
from uuid import UUID
from .proto_http import ProtoHttp
from .Cloud import Cloud
from .handler import handleFiwareResponse
__all__=[]

def _omit(json, arr):
	return {k: v for k,v in json.items() if k not in arr}

def omitDeviceParameters(device):
	return _omit(device,['type',
	'isPattern',
	'attributes'
	])

def parseAttributes(attributes):
	attrParsed = {}
	for attr in attributes:
		attrParsed[attr.get('name')] = attr.get('value')
	return attrParsed

def omitDevicesParameters(devices):
	for i,dev in enumerate(devices):
		dev = dev.get('contextElement')
		dev.update(parseAttributes(dev.get('attributes')))
		devices[i] = omitDeviceParameters(dev)

	return devices

def authHttpHeaders(credentials):
	return {
		'fiware-service': "knot",
		'fiware-servicepath': "/device/%s" %credentials.get('id') if credentials.get('id') else '/device',
	}

def addDevice():
	return {'type': 'POST', 'endpoint':'/v2/entities'}

def rmDevice(device):
	return {'type': 'POST', 'endpoint':'/v1/updateContext'}

def listDevice():
	return {'type': 'POST', 'endpoint':'/v1/queryContext'}

def updateDevice(device):
	return {'type': 'POST', 'endpoint':'/v1/updateContext'}

def listData(device):
	return {'type': 'GET', 'endpoint': '/v2/entities/%s?options=keyValues' %device}

def addData(device):
	return {'type': 'POST', 'endpoint': '/data/%s' %device}

def subs(device):
	return {'type': 'POST', 'endpoint': 'v2/subscriptions'}

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
		user_data = {
			'id': 'knot',
			'type': 'device',
		}
		return self.protocol.registerDevice(credentials, user_data)

	def unregisterDevice(self, credentials, uuid, user_data={}):
		body = {
			"contextElements": [
				{
					"type": "device",
					"isPattern": "false",
					"id": uuid,
				}
			],
			"updateAction": "DELETE"
		}# logging.error('Missing implementation')
		return self.protocol.unregisterDevice(credentials, uuid, body)
                #{'payload': {'id': uuid}})

	def update(self, credentials, uuid, user_data={}):
		body = {
			"contextElements": [
				{
					"type": "device",
					"isPattern": "false",
					"id": uuid,
					"attributes": [
						{
							"name": "setProperties",
							"type": "command",
							"value": user_data
						}
					]
				}
			],
			"updateAction": "UPDATE"
		}
		response = self.protocol.update(credentials, uuid, body).get('contextResponses')
		return handleFiwareResponse(response)

	def listSensors(self, credentials, thing_uuid):
		body = {
			"entities": [
				{
					"type": "sensor",
					"isPattern": "true",
					"id": "/*"
				}
			]
		}
		credentials['id'] = thing_uuid
		response = self.protocol.listDevice(credentials, thing_uuid, body).get('contextResponses')
		return handleFiwareResponse(response)

	def getSensorDetails(self, credentials, thing_uuid, sensor_id):
		body = {
			"entities": [
				{
					"type": "sensor",
					"isPattern": "true",
					"id": str(sensor_id)
				}
			]
		}
		credentials['id'] = thing_uuid
		response = self.protocol.listDevice(credentials, thing_uuid, body).get('contextResponses')
		return handleFiwareResponse(response)


	def getThings(self, credentials, gateways=['*']):
		body = {
			'entities': [
				{
					'type': 'device',
					'isPattern': 'true',
					'id': '/*'
				}
			]
		}
		response = self.protocol.myDevices(credentials, body).get('contextResponses')
		if response:
			return omitDevicesParameters(response)
		else:
			raise Exception('No device was found')

	def requestData(self, credentials, thing_uuid, sensor_id):
		body = {
			"contextElements": [
				{
					"type": "sensor",
					"isPattern": "false",
					"id": sensor_id,
					"attributes": [
						{
							"name": "getData",
							"type": "command",
							"value": ""
						}
					]
				}
			],
			"updateAction": "UPDATE"
		}
		credentials['id'] = thing_uuid
		response = self.protocol.update(credentials, thing_uuid, body).get('contextResponses')
		return handleFiwareResponse(response)

	def setConfig(self, credentials, thing_uuid, sensor_id,
					eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0):
		logging.error('Missing implementation')
		body = {
			"contextElements": [
				{
					"type": "device",
					"isPattern": "false",
					"id": sensor_id,
					"attributes": [
						{
							"name": "setConfig",
							"type": "command",
							"value": {
								"sensor_id": sensor_id,
								"event_flags": eventFlags,
								"time_sec": timeSec,
								"lower_limit": lowerLimit,
								"upper_limit": upperLimit
							}
						}
					]
				}
			],
			"updateAction": "UPDATE"
		}
		credentials['id'] = thing_uuid
		response = self.protocol.update(credentials, thing_uuid, body).get('contextResponses')
		return handleFiwareResponse(response)

	def getData(self, credentials, thing_uuid, **kwargs):
		logging.error('Missing implementation')
		pass
	def subscribe(self, credentials, uuid, onReceive=None):
		logging.error('Missing implementation')
		pass
	def postData(self, credentials, thing_uuid, user_data={}):
		logging.error('Missing implementation')
		pass
	def setData(self, credentials, thing_uuid, sensor_id, value):
		body = {
			"contextElements": [
				{
					"type": "sensor",
					"isPattern": "false",
					"id": sensor_id,
					"attributes": [
						{
							"name": "setData",
							"type": "command",
							"value": value
						}
					]
				}
			],
			"updateAction": "UPDATE"
		}
		credentials['id'] = thing_uuid
		response = self.protocol.update(credentials, thing_uuid, body).get('contextResponses')
		return handleFiwareResponse(response)
