from __future__ import print_function
import socket
from datetime import datetime


#replace it with aws server address
host = "localhost"
port= 14000


class client:
	def __init__(self,server_ip,server_port):
		self.server_ip = server_ip
		self.server_port = server_port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		 
	
	def ping_server(self,msg):
		self.sock.sendto(msg, (host, port))
		data,addr = self.sock.recvfrom(1024)
		print(data,addr)
		return True


local_client = client(host,port)
local_client.ping_server("TEST")
