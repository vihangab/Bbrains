#!/usr/bin/env python
import socket
import struct
import sys

UDP_PORT=15000

sockfd = socket.socket(socket.AF_NET,socket.SOCK_DGRAM)
sockfd.bind = ('',UDP_PORT)
print "Listening on port " + str(UDP_PORT)

client_request = []

while True:
    data, addr = sockfd.recvfrom(1024)
    client_requests.append(addr)
    print "Connection from " + str(addr)
    

