#!/usr/bin/env python

import socket
import struct
import time
import sys

aws_ip=("10.234.37.210",15000)

try:
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sockfd.bind(('',0))
    sockfd.sendto("hello",aws_ip)

except socket.error:
    print "failed to create socket" + str(socket.error)
    sys.exit()

peer_data,addr = sockfd.recvfrom(1024)
print peer_data

print "trying to connect to peer"
peer_ip = peer_data.split(':')[0]
peer_port = peer_data.split(':')[1]

for i in range(100):
    print "sending packets"
    sockfd.sendto("hello from client A , ",(peer_ip,peer_port))
    time.sleep(1)


    
