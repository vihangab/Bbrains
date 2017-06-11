#!/usr/env python

# Author : Vihanga Bare #
import socket 
import json
from pprint import pprint

host = '127.0.0.1' 
port = 8888
BUFFER_SIZE = 1024

MESSAGE = raw_input("tcpClient: Enter message/ Enter exit:") 
 
tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClient.connect((host, port))
 
while MESSAGE != 'exit':
    tcpClient.send(MESSAGE)     
    data = tcpClient.recv(BUFFER_SIZE)
    print " Client received data:", data
    MESSAGE = raw_input("tcpClient: Enter command to continue/ Enter exit:")
 
tcpClient.close()
