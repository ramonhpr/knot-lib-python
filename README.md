# KNoT lib python

### A library to access data from KNoT supported clouds

## How to install

```s
$ sudo pip install git+http://github.com/ramonhpr/knot-lib-python@master
```

If you don't have sudo access:

```s
$ sudo pip install virtualenv
$ virtualenv ~/envname
$ . ~/envname/bin/activate
$ pip install .
```
## Quick Start
This API can access the cloud selected in platform KNoT and find data about KNoT devices by a simple client connection.

KNoT can now support two protocol to get data from things:

* http
* socketio

KNoT can now support two clouds:
* Meshblu
* Fiware (just support to IoT agent and orion GE's)

In KNoT webui you can find your credentials

```python
    from knotpy import KnotConnection
    credentials = {
            'servername': 'knot-test.cesar.org.br',
            'port': 3000,
            'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
            'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
    }
    conn = KnotConnection(credentials)
    myThings = conn.getDevices()
```

## Objects

### KnotConnection(credentials[, cloud='MESHBLU', protocol='socketio'])

Create a client object that will connect to a KNoT Cloud instance.

#### Arguments

* `credentials` **dict** The credentials used to authenticate with each cloud
  * `servername` **string** Cloud instance hostname
  * `port` **int** Cloud instance port
  * [`uuid`] **string** uuid of meshblu user
  * [`token`] **string** token of meshblu user
* `cloud` **string** One of the cloud supported by KNoT platform.
Default: Meshblu .Supports: ['Meshblu', 'Fiware']
* `protocol` **string** One of the protocol supported.
Default: Socket.IO. Supports: ['http', 'socketio']

#### Example

```python
from knotpy import KnotConnection
credentials = {
            'servername': 'knot-test.cesar.org.br',
            'port': 3000,
            'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
            'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
```

## Methods

### getDevices():list

Gets the devices associated to the connected user.

#### Result

* `devices` **list** devices registered on the cloud or an empty list. Each device is an object in the following format:
  * `id` **String** device ID (KNoT ID).
  * `name` **String** device name.
  * `online` **Boolean** whether this device is online or not.

#### Example

```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  myDevices = conn.getDevices()
except Exception as err:
  print(err)
# [ { online: true,
#    name: 'Door lock',
#    id: '7e133545550e496a',
#    schema: [ [Object], [Object] ] } ]
```

### listSensors(id):list
List the sensor by a device identified by id.

#### Arguments
* `id` **String** device ID (KNoT ID).

#### Result
* `sensors` **list** list of int
  * `id` **int** sensor ID

#### Example
```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  sensors = conn.listSensors('7e133545550e496a')
except Exception as err:
  print(err)
# [1,2]
```

### getSensorDetails(id, sensorId):dict
Gets the sensor details from a specific sensor identified.

#### Argument
* `id` **String** device ID (KNoT ID).
* `sensor_id` **int** sensor ID.

#### Result

* `schema` **list** schema items, each one formed by:
  * `sensor_id` **int** sensor ID.
  * `value_type` **int|float|bool** semantic value type (voltage, current, temperature, etc).
  * `unit` **int** sensor unit (V, A, W, etc).
  * `type_id` **int** data value type (boolean, integer, etc).
  * `name` **string** sensor name.

#### Example
```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  sensors = conn.listSensors('7e133545550e496a')
  for sensor_id in sensors:
    print(conn.getSensorDetails('7e133545550e496a', sensor_id))
except Exception as err:
  print(err)
# { sensor_id: 1,
#   value_type: 3,
#   unit: 0,
#   type_id: 65521,
#   name: 'Lock' }
# { sensor_id: 2,
#   value_type: 1,
#   unit: 2,
#   type_id: 9,
#   name: 'Card reader' }
```
### getData(id[,limit=10, start, finish]):list

Gets the last 10 data items published by the device identified by id.

##### Arguments

* `id` **String** device ID (KNoT ID).
* `limit` **String** (Optional) the maximum number of data that you want, default=`10` (the value `*` returns all data)
* `start` **String** (Optional) the start date that you want your set of data (format=`YYYY/MM/DD HH:MM`)
* `finish` **String** (Optional) the finish date that you want your set of data (format=`YYYY/MM/DD HH:MM`)

##### Result

* `data_items` **list** data items published by the device or an empty list. Each data item is an object in the following format:
  * `data` **dict** data published by the device, in the following format:
    * `sensor_id` **int** sensor ID.
    * `value` **String|Boolean|float|int** value published.
  * `timestamp` **Date** moment of publication.

#### Example
```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  myDevices = conn.getData('7e133545550e496a')
except Exception as err:
  print(err)
# [ { data: { sensor_id: 2, value: 0 },
#     timestamp: '2018-08-25T05:29:43.519Z' },
#   { data: { sensor_id: 1, value: true },
#     timestamp: '2018-08-25T05:29:43.520Z' },
#     ... ]
```
### setData(id, sensorId, value)
Sets a value to a sensor.

##### Argument

* `id` **String** device ID (KNoT ID).
* `sensorId` **String** sensor ID.
* `value` **String|Boolean|Number** value to attribute to the sensor.

##### Example
```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  myDevices = conn.setData('7e133545550e496a', 1, True)
except Exception as err:
  print(err)
```

### requestData(id, sensorId)
Requests the device to publish its current value of a sensor. The value can be retrieved using `getData()` or by listening to device updates.

##### Argument

* `id` **String** device ID (KNoT ID).
* `sensorId` **String** sensor ID.

#####  Example
```python
from knotpy import KnotConnection
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  myDevices = conn.requestData('7e133545550e496a', 1)
except Exception as err:
  print(err)
```

### sendConfig(id, sensorId[, eventFlags=8, timeSec=0, lowerLimit=0, upperLimit=0])
Send configuration from the sensor of your thing if it is online


#### Argument

* `id` **String** device ID (KNoT ID).
* `sensorId` **String** sensor ID.
* `eventFlags` **int**
You can use the event flags macro bellow:
  * `FLAG_TIME`: Send data every period of time, in seconds. Needs a value greater than 0 to be passed on time_sec
  * `FLAG_LOWER`: Send data every time that the item is below a threshold. The value to be compared with is the one passed on lower_limit. If combined with `FLAG_UPPER`, **it is mandatory that lower_limit is smaller than upper_limit**.
  * `FLAG_UPPER`: Send data every time that the item is above a threshold. The value to be compared with is the one passed on upper_limit. If combined with `FLAG_LOWER`, **it is mandatory that lowerLimit is smaller than upperLimit**.
  * `FLAG_CHANGE`: Send data every time the item changes its value. Does not require any additional field.
  * `FLAG_MAX`: Send all the other above
* `timeSec` **int** the time in seconds when a sensor will publish a data. If `FLAG_TIME` is set, this field is mandatory
* `lowerLimit` **int** the threshold value when a sensor will publish bellow this value. If `FLAG_LOWER` is set, this field is mandatory
* `upperLimit` **int** the threshold value when a sensor will publish above this value. If `FLAG_UPPER` is set, this field is mandatory

#####  Example
```python
from knotpy import *
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)
try:
  myDevices = conn.sendConfig('7e133545550e496a', 1, eventFlag=FLAG_TIME+FLAG_CHANGE, timeSec=30)
except Exception as err:
  print(err)
```

### subscribe(id, onReceive)

Subscribes to data published by a device identified by id. To listen to the publish events, register a callback in parameter onReceive.

#### Argument

* `id` **string**
* `onReceive` **function** Callback function called with device updates. Receives:
  * `event` **dict** published event, object in the following format:
    * `source` **String** device ID (KNoT ID).
    * `data` **dict** data published by the device, in the following format:
      * `sensor_id` **Number** sensor ID.
      * `value` **String|Boolean|Number** value published.
    * `timestamp` **Date** moment of publication.

#### Example
```python
from knotpy import *
credentials = {
  'servername': 'knot-test.cesar.org.br',
  'port': 3000,
  'uuid': 'bf3aed9f-c52e-4bc5-9021-f5065acc0000',
  'token': '0bd12a4c31de141909c3dd955d6b881d5ca5fa5b'
}
conn = KnotConnection(credentials)

def callback(event):
  print(event)

try:
  myDevices = conn.subscribe('7e133545550e496a', callback)
except Exception as err:
  print(err)
# { data: { sensor_id: 2, value: 21 },
#   timestamp: '2018-08-25T17:46:41.337Z',
#   source: '7e133545550e496a' }
```

----------

# LOG LEVEL
You can enable two log levels in knotpy, INFO and DEBUG, by adding a environment
variable. In INFO log you can
enable messages in the package knotpy. And in DEBUG log you can also see the
log levels in the other dependencies packages.
