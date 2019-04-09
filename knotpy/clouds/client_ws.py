import ssl
import json
from websocket import create_connection

class ClientWs(object):
    def __init__(self, hostname, port):
        self.protocol = 'wss' if port == 443 else 'ws'
        self.socket = create_connection(
            '%s://%s:%d' %(self.protocol, hostname, port),
            sslopt={'cert_reqs': ssl.CERT_NONE}
        )

    def send_frame(self, type_frame, data):
        self.socket.send(json.dumps({'type': type_frame, 'data': data}))

    def once(self, type_frame, callback):
        data = json.loads(self.socket.recv())
        if data.get('type') == type_frame:
            callback(data.get('data'))
        elif data.get('type') == 'error':
            raise Exception(data.get('data'))
