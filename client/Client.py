import urllib2
import urllib
import time

#HOST
HOST = "http://localhost:5000"
#Local: http://localhost:5000
#Remote: http://54.200.177.96

#The identifier of this device
DEVICE_KEY = "umoeder"

#Sensors
SENSOR_LIGHT = "light"
SENSOR_TEMPERATURE = "temperature"
SENSOR_HUMIDITY = "humidity"
SENSOR_CAMERA = "camera"

def postSensorData(sensor, value):
    now = time.time()
    getRequestParameters = { "deviceKey" : DEVICE_KEY, "sensortype" : sensor, "value" : value, "date" : time.time() }
    
    response = urllib2.urlopen(HOST + '/sensorData/postSensorData?' + urllib.urlencode(getRequestParameters))
    html = response.read()
    print html
    
postSensorData(SENSOR_HUMIDITY, "666")

'''
conn = httplib.HTTPConnection("http://localhost:5000")
myParameters = { "deviceKey" : "umoeder", "sensortype" : "temperature", "value" : "35", "date" : "1385645805477" }
print "/sensorData/postSensorData?" + urllib.urlencode(myParameters)
conn.request("GET", "/sensorData/postSensorData?" + urllib.urlencode(myParameters))
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
conn.request("GET", "/parrot.spam")
r2 = conn.getresponse()
print r2.status, r2.reason
data2 = r2.read()
conn.close()
'''
