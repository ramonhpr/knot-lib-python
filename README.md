# KNoT lib python

### Use meshblu API to access devices data in KNoT platform

## How to install

```s
$ sudo pip install virtualenv
$ virtualenv ~/envname
$ . ~/envname/bin/activate
$ pip install .
```
## Description
```python
    This API can access the meshblu and find data about KNoT devices
    by a simple client connection.

    KNoT can now support two protocol to get data from things:
            - http
            - socketio

    In KNoT webui you can find your credentials
    See an example:
    > from knotpy import KnotConnection
    > credentials = {
            'servername': '<your_local_IP>/<raspberry_IP>',
            'port': 3000,
            'uuid': <user_uuid>,
            'token': <user_token>
    }
    > conn = KnotConnection(credentials, protocol='http')
    > myThings = conn.getThings()

    `myThings` is an array with the things that is online and offline in your gateway
    This things have informations like your id, if they are online or no, and the
    sensors of this things.
```

## API functions
```python
class KnotConnection(__builtin__.object)
     |  This is the main class to connect to KNoT Cloud
     |  KnotConnection(protocol, credentials)
     |
     |  Methods defined here:
     |
     |  __init__(self, credentials, cloud='MESHBLU', protocol='socketio')
     |
     |  getData(self, thing_uuid, **kwargs)
     |      Get thing data from cloud and
     |      return a list of dict/json with your data
     |      You can pass querys to this function by using:
     |              - limit: the maximum number of data that you want, default=10
     |              - start: the start date that you want your set of data
     |              - finish: the finish date that you want your set of data
     |      Examples:
     |      conn.getData(thing_uuid, limit=1) # get most recent data from your sensor
     |      conn.getData(thing_uuid, finish='2018/03/15') # get data the 10 data from until this date
     |
     |  getThings(self)
     |      Get the things of your user
     |
     |  myDevices(self)
     |      Return all devices of your gateway
     |      Note:
     |              If you run it in the cloud it returns the gateway device
     |              If you run it in the fog it returns all the devices of your gateway
     |
     |  postData(self, thing_uuid, user_data={})
     |      Post the json passed in user_data to the cloud
     |
     |  registerDevice(self, user_data={})
     |      Register a device in the cloud with owner credentials
     |      and return a dict/json with the device added
     |
     |  sendConfig(self, thing_uuid, sensor_id, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0)
     |      Send configuration from the sensor of your thing if it is online
     |      You can use the event flags macro bellow:
     |      FLAG_TIME
     |      FLAG_LOWER
     |      FLAG_UPPER
     |      FLAG_CHANGE
     |      FLAG_MAX
     |
     |  sendGetData(self, thing_uuid, sensor_id)
     |      Force your thing to post sensor data indepent of your configuration
     |
     |  setData(self, thing_uuid, sensor_id, value)
     |      Set data of the sensor from your thing
     |
     |  subscribe(self, uuid, onReceive=None)
     |      Subscribe the device to monitor changes on it
     |
     |  unregisterDevice(self, user_data={})
     |      Unregister a device with the credentials passed by the dict/json
     |      parameter and return the successed json message
     |
     |  update(self, uuid, user_data={})
     |      Update a device with the credentials passed by the dict/json
     |      parameter and return the successed json message
     |

```

# LOG LEVEL
You can enable two log levels in knotpy, INFO and DEBUG, by adding a environment
variable. In INFO log you can
enable messages in the package knotpy. And in DEBUG log you can also see the
log levels in the other dependencies packages.
