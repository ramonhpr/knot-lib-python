import requests

class ProtoHttp(object):
    def __parseUrl(self, credentials):
        return 'http://'+credentials.get('servername')+':'+str(credentials.get('port'))
    def registerDevice(self, credentials, user_data={}):
        response = requests.post(self.__parseUrl(credentials) + '/devices', json=user_data)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            raise Exception('Http Error')