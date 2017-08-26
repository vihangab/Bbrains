#!/usr/bin/env python

#import required modules
from __future__ import print_function # Python 2/3 compatibility
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
import time
import paho.mqtt.client as paho
import ssl
import boto3
import json
import datetime
import json
from time import sleep
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

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

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')#, endpoint_url="https://dynamodb.us-east-1.amazonaws.com/")
table = dynamodb.Table('RpiZero_DB')
print("Accessing Rpi3 db")

#Define handlers for MQTT events
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

#Set the keys and certificates for MQTT thing
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while  1==1:
    sleep(10)
    date_update = datetime.datetime.now().strftime("%Y%m%d")
    time_update= datetime.datetime.now().strftime("%H:%M")
    temperature = 26
    result_json = {
  	"Date":date_update,
  	"Time":time_update,
  	"Temperature":temperature,
  }
    mqttc.publish("temperature", json.dumps(result_json), 0)
    print("msg sent: temperature " + str(temperature))
    
