#!/usr/bin/env python

#import required modules
from __future__ import print_function # Python 2/3 compatibility
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
import time
import paho.mqtt.client as paho
import ssl
import json
import datetime
import json
from time import sleep

class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return super(PythonObjectEncoder, self).default(self)#{'_python_object': pickle.dumps(obj)}

class SetEncoder(json.JSONEncoder):
     def default(self, obj):
          if isinstance(obj, set):
             return list(obj)
          return json.JSONEncoder.default(self, obj)


# Define handlers for MQTT events
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

#Keys and certificate for AWS IoT
awshost = "aekn89lpwmp2q.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "temperature"
thingName = "temperature"
caPath = "VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
certPath = "febe95c28b-certificate.pem.crt"
keyPath = "febe95c28b-private.pem.key"

#Set the keys and certificates for MQTT publishing to AWS IOT thing
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    sleep(10)
    date_update = datetime.datetime.now().strftime("%Y%m%d")
    time_update= datetime.datetime.now().strftime("%H:%M")
    mqttc.publish("temperature", 26, qos=0)
    print("msg sent: temperature " + str(26))
    
