import requests
import logging
import json
from uuid import UUID
from .proto import KnotProtocol
__all__=[]

class ProtoHttp(KnotProtocol):
	def __parseUrl(self, credentials):
		return 'http://'+credentials.get('servername')+':'+str(credentials.get('port'))

	def __queryParameter(self, data):
		ret = '?'
		logging.info(data)
		for key in data:
			ret = ret + key + '=' + str(data.get(key)) + '&'
		return ret

	def __init__(self, headers, addDev, rmDev, listDev, updateDev, addData, listData, subs):
		# Callbacks helpers
		self.cloudHeaders = headers
		self.addDev = addDev
		self.rmDev = rmDev
		self.listDev = listDev
		self.updateDev = updateDev
		self.addData = addData
		self.listData = listData
		self.subs = subs

	def __doRequest(self, headers, url, typeReq, body, stream=False):
		logging.info('%s %s' %(typeReq, url))
		logging.info('json -> '+ str(body))
		logging.info('Headers ' + str(headers))
		if typeReq == 'POST':
			response = requests.post(url, headers=headers, json=body)
		elif typeReq == 'GET':
			response = requests.get(url, headers=headers, stream=stream)
			if stream:
				return response
		elif typeReq == 'PUT':
			response = requests.put(url, headers=headers, json=body)
		elif typeReq == 'DELETE':
			response = requests.delete(url, headers=headers, json=body)
		logging.info('status_code -> ' + str(response.status_code))

		try:
			logging.info('response_json -> ' + str(response.json()))
			return response.json()
		except:
			logging.info('response_text-> ' + str(response.text))
			return response.text

	def registerDevice(self, credentials, user_data={}):
		url = self.__parseUrl(credentials) + self.addDev()['endpoint']
		typeReq = self.addDev()['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, user_data)

	def unregisterDevice(self, credentials, device_id, user_data={}):
		url = self.__parseUrl(credentials) + self.rmDev(device_id)['endpoint']
		typeReq = self.rmDev(device_id)['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, user_data)

	def myDevices(self, credentials, user_data={}):
		url = self.__parseUrl(credentials) + self.listDev()['endpoint']
		typeReq = self.listDev()['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, user_data)

	def subscribe(self, credentials, device_id, onReceive=None):
		url = self.__parseUrl(credentials) + self.subs(device_id)['endpoint']
		typeReq = self.subs(device_id)['type'].upper()
		with self.__doRequest(self.cloudHeaders(credentials), url, typeReq, {}, True) as response:
			logging.info('status_code -> ' + str(response.status_code))
			try:
				for line in response.iter_lines():
					if line:
						line_decoded = line.decode('utf-8')
						logging.info('Received ' + line_decoded)
						onReceive(json.loads(line_decoded))
			except KeyboardInterrupt:
				pass

	def update(self, credentials, device_id, user_data={}):
		url = self.__parseUrl(credentials) + self.updateDev(device_id)['endpoint']
		typeReq = self.updateDev(device_id)['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, user_data)

	def getData(self, credentials, device_id, **kwargs):
		url = self.__parseUrl(credentials) + self.listData(device_id)['endpoint']
		typeReq = self.listData(device_id)['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, kwargs)

	def postData(self, credentials, device_id, user_data={}):
		url = self.__parseUrl(credentials) + self.addData(device_id)['endpoint']
		typeReq = self.addData(device_id)['type'].upper()
		return self.__doRequest(self.cloudHeaders(credentials), url, typeReq, user_data)

