import logging
import json
import requests
from .proto import Protocol
__all__ = []

class ProtoHttp(Protocol):
    @classmethod
    def __parse_url(cls, credentials):
        return 'http://'+credentials.get('servername')+':'+str(credentials.get('port'))

    @classmethod
    def __query_parameter(cls, data):
        ret = '?'
        logging.info(data)
        for key in data:
            ret = ret + key + '=' + str(data.get(key)) + '&'
        return ret

    def __init__(self, headers, add_dev, rm_dev, list_dev, update_dev, add_data, list_data, subs):
        # Callbacks helpers
        self.cloud_headers = headers
        self.add_dev = add_dev
        self.rm_dev = rm_dev
        self.list_dev = list_dev
        self.update_dev = update_dev
        self.add_data = add_data
        self.list_data = list_data
        self.subs = subs

    @classmethod
    def __do_request(cls, headers, url, type_req, body, stream=False):
        logging.info('%s %s', type_req, url)
        logging.info('json -> %s', body)
        logging.info('Headers %s', headers)
        if type_req == 'POST':
            response = requests.post(url, headers=headers, json=body)
        elif type_req == 'GET':
            response = requests.get(url, headers=headers, stream=stream)
            if stream:
                return response
        elif type_req == 'PUT':
            if body:
                response = requests.put(url, headers=headers, json=body)
            else:
                response = requests.put(url, headers=headers)

        elif type_req == 'DELETE':
            if body:
                response = requests.delete(url, headers=headers, json=body)
            else:
                response = requests.delete(url, headers=headers)

        logging.info('status_code -> %d', response.status_code)

        try:
            logging.info('response_json -> %s', response.json())
            return response.json()
        except ValueError:
            logging.info('response_text-> %s', response.text)
            return response.text

    def register_device(self, credentials, user_data=None):
        url = self.__parse_url(credentials) + self.add_dev()['endpoint']
        type_req = self.add_dev()['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, user_data)

    def unregister_device(self, credentials, device_id, user_data=None):
        url = self.__parse_url(credentials) + self.rm_dev(device_id)['endpoint']
        type_req = self.rm_dev(device_id)['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, user_data)

    def my_devices(self, credentials, user_data=None):
        url = self.__parse_url(credentials) + self.list_dev()['endpoint']
        type_req = self.list_dev()['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, user_data)

    def subscribe(self, credentials, device_id, on_receive=None):
        url = self.__parse_url(credentials) + self.subs(device_id)['endpoint']
        type_req = self.subs(device_id)['type'].upper()
        with self.__do_request(self.cloud_headers(credentials), url, type_req, {}, True) as res:
            logging.info('status_code -> %d', res.status_code)
            try:
                for line in res.iter_lines():
                    if line:
                        line_decoded = line.decode('utf-8')
                        logging.info('Received %s', line_decoded)
                        on_receive(json.loads(line_decoded))
            except KeyboardInterrupt:
                pass

    def update(self, credentials, device_id, user_data=None):
        url = self.__parse_url(credentials) + self.update_dev(device_id)['endpoint']
        type_req = self.update_dev(device_id)['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, user_data)

    def get_data(self, credentials, device_id, **kwargs):
        url = self.__parse_url(credentials) + self.list_data(device_id)['endpoint']
        type_req = self.list_data(device_id)['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, kwargs)

    def post_data(self, credentials, device_id, user_data=None):
        url = self.__parse_url(credentials) + self.add_data(device_id)['endpoint']
        type_req = self.add_data(device_id)['type'].upper()
        return self.__do_request(self.cloud_headers(credentials), url, type_req, user_data)
