class Protocol(object):
    def register_device(self, credentials, user_data=None):
        pass
    def unregister_device(self, credentials, device_id, user_data=None):
        pass
    def my_devices(self, credentials, user_data=None):
        pass
    def update(self, credentials, device_id, user_data=None):
        pass
    def post_data(self, credentials, device_id, user_data=None):
        pass
    def subscribe(self, credentials, device_id, on_receive=None):
        pass
    def get_data(self, credentials, device_id, **kwargs):
        pass
