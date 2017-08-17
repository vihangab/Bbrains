#!/usr/bin/env python

import paho.mqtt.client as paho
import os
import socket
import ssl

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

mqttc.loop_forever()
