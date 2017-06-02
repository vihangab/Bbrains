#!/usr/bin/env python
from socket import *
import threading
import time

class serverThread(threading.Thread):
    def __init__(self, serverPort):
        threading.Thread.__init__(self)
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.connectionThreads = []
    def run(self):
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(1)
        while True:
            #Establish the connection
            print 'Ready to serve...'
            connectionSocket = self.serverSocket.accept()
            message = connectionSocket.recv(1024) #Get message
            print "Message recieved, opening new thread"
            self.connectionThreads.append(connectionThread())
            self.connectionThreads[len(connectionThreads)-1].start()
    def close(self):
        for t in self.connectionThreads:
            t.close()
        self.serverSocket.close()

class connectionThread (threading.Thread):
    def __init__(self, connSocket, message):
        threading.Thread.__init__(self)
        self.connSocket = connSocket
        self.message = message
    def run(self):
        try:
            filename = self.message.split()[1] #Getting requested HTML page
            f = open(filename[1:]) #Opening data stream from HTML
            outputdata = f.read() #Reading HTML page
            f.close() #Closing data stream from HTML
            self.connSocket.send("HTTP/1.0 200 OK\r\n") #Send one HTTP header line into socket
            for i in range(0, len(outputdata)): #Send the content of the requested file to the client
                self.connSocket.send(outputdata[i])
        except IOError: #Triggered if user requests bad link
            self.connSocket.send("404 Not Found") #Send response message for file not found
        finally:
            self.connSocket.close()

def main():
    server = serverThread(8031)
    server.start()
    end = raw_input("Press enter to stop server...")
    server.close()
    print "Program complete"

main()
