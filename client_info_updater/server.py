
from __future__ import print_function
import socket
from datetime import datetime

host_ip =socket.gethostbyname(socket.gethostname())

UDP_PORT = 14000


class server:
	def __init__(self,port_number):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.bind(("localhost",port_number))

	def listen(self):
		while True:
			data,addr = self.sock.recvfrom(1024)
			print(data,addr)
			if data == 'TEST':
				reply = str(datetime.now())
				self.sock.sendto(reply,addr)
				
local_server = server(UDP_PORT)
local_server.listen()