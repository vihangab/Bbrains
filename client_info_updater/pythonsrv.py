#!/usr/bin/env python
import socket
import struct
import sys

UDP_PORT=15000

sockfd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sockfd.bind(('',UDP_PORT))
print "Listening on port " + str(UDP_PORT)

client_requests = []

while True:
    data, addr = sockfd.recvfrom(1024)
    client_requests.append(addr)
    print "Connection from " + str(addr)
    if client_requests == 2:
	break

clientA_ip=client_requests[0][0]
clientA_port=client_requests[0][1]
#clientB_ip=client_requests[1][0]
#clientB_port=client_requests[1][1]

sockfd.sendto(str(clientA_ip) + ":" + str(clientA_port), client_requests[1])
sockfd.close()

    

