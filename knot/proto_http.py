import requests

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
        response = requests.post(self.__parseUrl(credentials) + '/devices', json=user_data)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            raise Exception('Http Error')

    def readData(self, credentials, thing_uuid, user_data={}):
        response = requests.get(self.__parseUrl(credentials) + '/data/' + thing_uuid + self.__queryParameter(user_data),
                                    headers=self.__authHeaders(credentials), json=user_data)
        return response.json()

    def postData(self, credentials, user_data={}):
        response = requests.post(self.__parseUrl(credentials) + '/data/' + user_data.get('uuid'),
                                    headers=self.__authHeaders(credentials), json=user_data)
