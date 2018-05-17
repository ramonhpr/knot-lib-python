import requests
import logging

class ProtoHttp(object):
    def __parseUrl(self, credentials):
        return 'http://'+credentials.get('servername')+':'+str(credentials.get('port'))
    def __authHeaders(self, credentials):
        return {
            'meshblu_auth_uuid': credentials.get('uuid'),
            'meshblu_auth_token': credentials.get('token')
        }
    def __queryParameter(self, data):
        ret = ''
        if data.get('query'):
            query = data.get('query')
            ret = ret + '?'
            for key in query:
                ret = ret + key + '=' + str(query.get(key)) + '&'
        return ret

    def registerDevice(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/devices'
        logging.info('POST ' + url)
        logging.info('json -> '+ str(user_data))
        response = requests.post(url, json=user_data)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            raise Exception('Http Error')

    def unregisterDevice(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/devices/' + user_data.get('uuid')
        logging.info('DELETE ' + url)
        response = requests.delete(url, headers=self.__authHeaders(credentials))
        logging.info('status_code -> ' + str(response.status_code))
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise Exception('Http Error')
        else:
            return response.text
    def myDevices(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/mydevices'
        logging.info('GET ' + url)
        response = requests.get(url, headers=self.__authHeaders(credentials))
        logging.info('json -> '+ str(user_data))
        logging.info('status_code -> ' + str(response.status_code))
        logging.info('response_json -> ' + str(response.json()))
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise Exception('Http Error')
        elif response.status_code == 401:
            return response.json()
        else:
            return response.text

    def readData(self, credentials, thing_uuid, user_data={}):
        url = self.__parseUrl(credentials) + '/data/' + thing_uuid + self.__queryParameter(user_data)
        logging.info('GET ' + url)
        logging.info('json -> '+ str(user_data))
        response = requests.get(url, headers=self.__authHeaders(credentials), json=user_data)
        return response.json()

    def postData(self, credentials, user_data={}):
        url = self.__parseUrl(credentials) + '/data/' + user_data.get('uuid')
        logging.info('POST ' + url)
        logging.info('json -> '+ str(user_data))
        response = requests.post(url, headers=self.__authHeaders(credentials), json=user_data)
