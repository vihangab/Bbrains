#!/usr/bin/env python3

###############################################################################################
# Authors: Vihanga Bare and Virag Gada
# File name : awsiotsub.py
# Description : File that is using MQTT protocol to subscribe data from AWS IOT Thing
# '/temperature'
# Use: Use this program with AWS IoT certificates and Thing
# keys to receive data from AWS IoT. Run using Python3.5 to support all the dependencies and
# libraries imported
# Program authenticates with AWS IOT thing using credentials  and subscribes data from
# AWS IOT thing.
# Please make sure you have Python 3.5.1 installed for all the
# below mentioned modules to work correctly with the integrated
# code
##############################################################################################

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

#awshost = "aekn89lpwmp2q.iot.us-west-2.amazonaws.com"
#awsport = 8883
#clientId = "VB_Rpi3"
#thingName = "VB_Rpi3"
#caPath = "root-CA.crt"
#certPath = "VB_Rpi3.cert.pem"
#keyPath = "VB_Rpi3.private.key"
# AWS IOT thing credentials
awshost = "a2vp65ivl2lw2v.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "MyRPi3"
thingName = "MyRPi3"
caPath = "root-CA.crt"
certPath = "MyRPi3.cert.pem"
keyPath = "MyRPi3.private.key"


mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
