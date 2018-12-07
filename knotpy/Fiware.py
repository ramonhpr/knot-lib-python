import logging
from uuid import UUID
from .proto_http import ProtoHttp
from .Cloud import Cloud
from .handler import handle_fiware_response
__all__=[]

def _omit(json, arr):
	return {k: v for k,v in json.items() if k not in arr}

def omitDeviceParameters(device):
	return _omit(device,['type',
	'isPattern',
	'attributes',
	'setConfig_status',
	'setConfig',
	'setProperties_status',
	'setConfig_info',
	'setProperties',
	'setProperties_info'
	])

def parseAttributes(attributes):
	attrParsed = {}
	for attr in attributes:
		if attr.get('type') ==  'number':
			attrParsed[attr.get('name')] = float(attr.get('value'))
		elif attr.get('type') ==  'boolean':
			attrParsed[attr.get('name')] = bool(attr.get('value'))
		else:
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

class Fiware(Cloud):
	def __init__(self, protocol):
		logging.info('Using protocol ' + protocol)
		self.iotagentPort = 4041
		self.protocol = {
			'http': ProtoHttp(
				headers=authHttpHeaders,
				addDev=lambda: {'type': 'POST', 'endpoint':'/v2/entities'},
				listDev=lambda: {'type': 'POST', 'endpoint':'/v1/queryContext'},
				rmDev=lambda device_id: {'type': 'DELETE', 'endpoint':'/v2/entities/%s' %device_id},
				updateDev=lambda device_id: {'type': 'POST', 'endpoint':'/v1/updateContext'},
				addData=lambda device_id: {'type': 'POST', 'endpoint': '/data/%s' %device_id},
				listData=lambda device_id: {'type': 'GET', 'endpoint': '/v2/entities/%s?options=keyValues' %device_id},
				subs=lambda: {'type': 'POST', 'endpoint': 'v2/subscriptions'})
		}.get(protocol.lower())

	def registerDevice(self, credentials, user_data={}):
		logging.error('Missing implementation')
		return
		user_data = {
			'id': 'knot',
			'type': 'device',
		}
		return self.protocol.registerDevice(credentials, user_data)

	def unregisterDevice(self, credentials, uuid, user_data={}):
		orionResponse = self.protocol.unregisterDevice(credentials, uuid, user_data)
		if orionResponse:
			return handle_fiware_response(orionResponse)

		tmpProtocol = self.protocol
		tmpProtocol.rmDev = lambda device: {'type': 'DELETE', 'endpoint': '/iot/devices/%s' %device}
		iotagentResponse = tmpProtocol.unregisterDevice({'servername': credentials['servername'], 'port': 4041}, uuid)
		if iotagentResponse:
			return handle_fiware_response(iotagentResponse)

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
		return handle_fiware_response(response)

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
		response = self.protocol.myDevices(credentials, body)
		try:
			if response.get('contextResponses'):
				devices = omitDevicesParameters(response.get('contextResponses'))
				return [{ 'id': sensor.get('id'), 'name': sensor.get('name') } for sensor in devices]
			else:
				return handle_fiware_response(response)
		except KeyError:
			return []
		except Exception as err:
			raise err



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
		response = self.protocol.myDevices(credentials, body)
		try:
			if response.get('contextResponses'):
				devices = omitDevicesParameters(response.get('contextResponses'))
				return [sensor for sensor in devices]
			else:
				return handle_fiware_response(response)
		except KeyError:
			return []
		except Exception as err:
			raise err


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
			raise Exception('Devices not found')

	def myDevices(self, credentials, gateways=['*']):
		return self.getThings(credentials, gateways)

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
		return handle_fiware_response(response)

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
		return handle_fiware_response(response)

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
		return handle_fiware_response(response)
