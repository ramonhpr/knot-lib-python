from .evt_flag import FLAG_CHANGE

class Cloud():
    def register_device(self, credentials, user_data=None):
        pass
    def unregister_device(self, credentials, device_id, user_data=None):
        pass
    def my_devices(self, credentials):
        pass
    def subscribe(self, credentials, device_id, on_receive=None):
        pass
    def update(self, credentials, device_id, user_data=None):
        pass
    def get_data(self, credentials, device_id, **kwargs):
        pass
    def post_data(self, credentials, device_id, user_data=None):
        pass
    def list_sensors(self, credentials, device_id):
        pass
    def get_sensor_detail(self, credentials, device_id, sensor_id):
        pass
    def get_things(self, credentials, gateways=None):
        pass
    def set_data(self, credentials, device_id, sensor_id, value):
        pass
    def request_data(self, credentials, device_id, sensor_id):
        pass
    def send_config(self, credentials, device_id, sensor_id, event_flags=FLAG_CHANGE, **kwargs):
        pass
