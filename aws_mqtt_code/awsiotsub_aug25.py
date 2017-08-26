#!/usr/bin/env python

import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import datetime
from time import sleep
import boto3
import decimal
import pickle


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

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')#, endpoint_url="https://dynamodb.us-west-2.amazonaws.com/")

table = dynamodb.Table('RPIZero_DB')

#handler which would be called when MQTT connection is established
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("temperature" , 1 )
#handler which would be called when MQTT message is received
def on_message(client, userdata, msg):
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

#AWS IOT Thing security credentials

#first you need to be authorised to connect to AWS IOT using access keys - AWS access key and aws secret key, which can be configured in .aws/credentials file
 
awshost = "aekn89lpwmp2q.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "temperature"
thingName = "temperature"
caPath = "VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
keyPath = "febe95c28b-private.pem.key"
certPath = "febe95c28b-certificate.pem.crt"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    sleep(100)
    date_update = datetime.datetime.now().strftime("%Y%m%d")
    time_update = datetime.datetime.now().strftime("%H:%M")
    response = table.get_item(Key={'Date':date_update,'Time':time_update})
    print(date_update)
    print(time_update)
    items = response['Item']['Temperature']


          
