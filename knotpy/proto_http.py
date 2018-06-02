import requests
import logging
import json
from uuid import UUID
__all__=[]

class ProtoHttp(object):
    def __parseUrl(self, credentials):
        return 'http://'+credentials.get('servername')+':'+str(credentials.get('port'))
    def __authHeaders(self, credentials):
        return {
            'meshblu_auth_uuid': credentials.get('uuid'),
            'meshblu_auth_token': credentials.get('token')
        }
    def __queryParameter(self, data):
        ret = '?'
        logging.info(data)
        for key in data:
            ret = ret + key + '=' + str(data.get(key)) + '&'
        return ret

    def registerDevice(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/devices'
        logging.info('POST ' + url)
        logging.info('json -> '+ str(user_data))
        try: # validate if uuid is in the right format
            UUID(credentials.get('uuid'), version=4)
        except ValueError as err:
            raise ValueError('Invalid credentials: ' + str(err))
        response = requests.post(url, json=user_data)
        logging.info('status_code -> ' + str(response.status_code))
        logging.info('response_json -> ' + str(response.json()))
        try:
            return response.json()
        except:
            return response.text

    def unregisterDevice(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/devices/' + user_data.get('uuid')
        logging.info('DELETE ' + url)
        response = requests.delete(url, headers=self.__authHeaders(credentials))
        logging.info('status_code -> ' + str(response.status_code))
        logging.info('response_json -> ' + str(response.json()))
        try:
            return response.json()
        except:
            return response.text

    def myDevices(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/mydevices'
        logging.info('GET ' + url)
        logging.info('json -> '+ str(user_data))
        response = requests.get(url, headers=self.__authHeaders(credentials))
        logging.info('status_code -> ' + str(response.status_code))
        logging.info('response_json -> ' + str(response.json()))
        try:
            return response.json()
        except:
            return response.text

    def subscribe(self, credentials, uuid, onReceive=None):
        url = self.__parseUrl(credentials) + '/subscribe/' + uuid
        logging.info('GET ' + url)
        with requests.get(url, headers=self.__authHeaders(credentials), stream=True) as response:
            logging.info('status_code -> ' + str(response.status_code))
            for line in response.iter_lines():
                if line:
                    line_decoded = line.decode('utf-8')
                    logging.info('Received ' + line_decoded)
                    onReceive(json.loads(line_decoded))

    def update(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/devices/' + user_data.get('uuid')
        logging.info('GET ' + url)
        logging.info('json -> ' + str(user_data))
        response = requests.put(url, headers=self.__authHeaders(credentials), json=user_data)
        logging.info('status_code -> ' + str(response.status_code))
        try:
            logging.info('response_json -> ' + str(response.json()))
            return response.json()
        except:
            logging.info('response_text-> ' + str(response.text))
            return response.text

    def readData(self, credentials, thing_uuid, **kwargs):
        url = self.__parseUrl(credentials) + '/data/' + thing_uuid + self.__queryParameter(kwargs)
        logging.info('GET ' + url)
        logging.info('json -> '+ str(kwargs))
        response = requests.get(url, headers=self.__authHeaders(credentials), json=kwargs)
        logging.info('status_code -> ' + str(response.status_code))
        logging.info('response_json -> ' + str(response.json()))
        try:
            return response.json()
        except:
            return response.text

    def postData(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/data/' + user_data.get('uuid')
        logging.info('POST ' + url)
        logging.info('json -> '+ str(user_data))
        response = requests.post(url, headers=self.__authHeaders(credentials), json=user_data)
        logging.info('status_code -> ' + str(response.status_code))
        try:
            return response.json()
        except:
            return response.text
