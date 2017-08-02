#!/usr/bin/env python
from __future__ import print_function
import socket
import sqlite3
from datetime import datetime

host_ip =socket.gethostbyname(socket.gethostname())

UDP_PORT = 14000



class server:
	def __init__(self,port_number):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
<<<<<<< HEAD
		self.sock.bind(("",UDP_PORT))
=======
		self.sock.bind(("",port_number))
>>>>>>> 05b0fdf42fad8dccf8d0c650c4155036d1339632

	def listen(self):
		while True:
			data,addr = self.sock.recvfrom(1024)
			if data == "TEST":
				print(data,addr)
				conn = sqlite3.connect("/home/ubuntu/client_info.db")
                                curr = conn.cursor()
                                sql=''' INSERT INTO ipaddress(ID,IP_ADDR,PORT_NO) VALUES(?,?,?) '''
				i=0
                                for item in addr:
					print(item)			
				reply = str(datetime.now())
				self.sock.sendto(reply,addr)
				#conn = sqlite3.connect("/home/ubuntu/client_info.db")
				#curr = conn.cursor()
				#sql=''' INSERT INTO ipaddress(ID,IP_ADDR,PORT_NO) VALUES(?,?,?) '''
				#value=(2,"0.0.0.0",2)
				#curr.execute(sql,value)
				break
local_server = server(UDP_PORT)
local_server.listen()
