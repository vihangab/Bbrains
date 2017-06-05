# run.py

# Author  : Vihanga Bare #

import socket
import os
import threading
import sys
import select
from signal import SIGINT
from flask import Flask, render_template, request
import random
import os
from app import create_app
port=8888


class Server:
#####-----Defining the Server-----#####    
    def __init__(self):
        self.host = ''
        self.port = port
        self.backlg = 5
        self.size = 1024
        self.server = None
        self.threads =[]

#####-----Opening the Server socket-----#####        
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.listen(5)
            print ("Waiting on port: " + str(port))
        except socket.error as e:
            if self.server:
                self.server.close()
            print ("Could not open socket: " + e.message)
            sys.exit(1)

#####-----Multi-threading in Server-----#####                         
    def run(self):
        self.open_socket()
        inputt = [self.server]
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(inputt,[],[])
            for s in inputready:
                if s == self.server:

#####-----Handle the server socket-----##### 
                    client,address = self.server.accept()
                    c = Client(client,address)
		    c.start()
                    self.threads.append(c)

#####-----Closing all the threads-----##### 
        self.server.close()
        for c in self.threads:
            c.join()

#####-----Defining the client class-----#####                         
class Client(threading.Thread):
    def __init__(self, c, address):
        threading.Thread.__init__(self)
        self.client = c
        self.address = address
        self.size = 1024

#####-----The main client program-----##### 
    def run(self):
        running = 1
        while running:
            try:
                request = []
                request = self.client.recv(self.size)
                while len(request) !=0 :
                    self.client.settimeout(60)
                    requestd=request.decode()
                    print("\n\nThe initial decoded request: "+requestd)
                    #self.client.settimeout(20)
                    print ("\nThis is the decoded request from the the Web Browser: \n" + requestd)
                    requestf = requestd.splitlines()[0]
                    requestf = requestf.rstrip('\r\n')
                    (command, fname, version) = requestf.split()
                    print ("\nCommand is: " + command)
                    print ("\nFile name requested is: " + fname)
                    print ("\nVersion of the request is: " + version)
            except:
                fh = open("http500ep.html", "rb")
                msg = fh.read()
                fh.close()
                cte4 = "text/html".encode()
                ste4 = os.stat("http500ep.html")
                cle4 = str(ste4.st_size).encode()
                http_response = b'HTTP/1.1 500 Internal Server Error\nContent-Type: '+(cte4)+b'\nContent-Length: '+(cle4)+b'\nConnection: Keep Alive\n\n'+msg
                self.client.send(http_response)

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)
    s = Server()
    s.run()
    if SIGINT:
	SIGKILL()
    
