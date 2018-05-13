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
