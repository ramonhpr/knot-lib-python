'''
KNoT Lib Python
'''
from .cloud_factory import CloudFactory
from .handler import handleEvtFlagError
from .evt_flag import FLAG_CHANGE
__all__ = ['KnotConnection']

class KnotConnection():
    '''This is the main class to connect to KNoT Cloud
    KnotConnection(credentials, protocol='http')
    '''
    def __init__(self, credentials, cloud='MESHBLU', protocol='socketio'):
        self.cloud = CloudFactory.init(cloud, protocol)
        self.credentials = credentials

    def unregister_device(self, device_id, user_data=None):
        '''
        Unregister a device with the credentials passed by the dict/json
        parameter and return the successed json message
        '''
        return self.cloud.unregisterDevice(self.credentials, device_id, user_data)

    def subscribe(self, device_id, on_receive=None):
        '''
        Subscribe the device to monitor changes on it
        '''
        self.cloud.subscribe(self.credentials, device_id, on_receive)

    def get_data(self, device_id, **kwargs):
        '''
        Get thing data from cloud and
        return a list of dict/json with your data
        You can pass querys to this function by using:
            - limit: the maximum number of data that you want, default=10
            - start: the start date that you want your set of data
            - finish: the finish date that you want your set of data
        Examples:
        conn.get_data(thing_uuid, limit=20, start='yesterday') # get 20 first data from yesterday
        conn.get_data(thing_uuid, limit=1) # get most recent data from your sensor
        conn.get_data(thing_uuid, finish='2018/03/15') # get data the 10 data from until this date
        '''
        result = self.cloud.getData(self.credentials, device_id, **kwargs)
        data = result.get('data')
        return data

    def list_sensors(self, device_id):
        '''
        Return a list of sensors from the thing_uuid
        '''
        return self.cloud.listSensors(self.credentials, device_id)

    def get_sensor_details(self, device_id, sensor_id):
        '''
        Return a detailed list of sensor_id
        '''
        return self.cloud.getSensorDetails(self.credentials, device_id, sensor_id)

    def get_devices(self):
        '''
        Get the devices of your user
        '''
        return self.cloud.getThings(self.credentials)

    def set_data(self, device_id, sensor_id, value):
        '''
        Set data of the sensor from your thing
        '''
        return self.cloud.setData(self.credentials, device_id, sensor_id, value)

    def request_data(self, device_id, sensor_id):
        '''
        Force your thing to post sensor data indepent of your configuration
        '''
        return self.cloud.requestData(self.credentials, device_id, sensor_id)

    def send_config(self, device_id, sensor_id, event_flags=FLAG_CHANGE, **kwargs):
        '''
        Send configuration from the sensor of your thing if it is online
        You can use the event flags macro bellow:
        FLAG_TIME
        FLAG_LOWER
        FLAG_UPPER
        FLAG_CHANGE
        FLAG_MAX
        '''
        time_sec = kwargs.get('time_sec')
        lower_limit = kwargs.get('lower_limit')
        upper_limit = kwargs.get('upper_limit')
        handleEvtFlagError(event_flags, time_sec, lower_limit, upper_limit)
        return self.cloud.setConfig(self.credentials, device_id, sensor_id,
                                    event_flags, time_sec, lower_limit, upper_limit)
