# Author  : Vihanga Bare #

import socket
import os
import threading
import sys
import select
from signal import SIGINT



#####-----Reading the configuration file and terminating program if absent-----#####
if os.path.isfile("ws.conf"):
    fh = open("ws.conf")
    line = fh.readlines()

#####-----Finding the port number-----#####
    portfound = line[1].rsplit()
    port = int(portfound[1])

#####-----Finding the complete path of document root-----#####
    patht = line[3].rsplit()
    prepath = patht[1]#+" "+patht[2]

#####-----Finding the webpage from configuration file-----#####
    webpt = line[5].rsplit()
    webp1 = webpt[1]
    webpf = "/" + webp1

#####-----Finding the content type for different extensions-----#####
    htmlt = line[7].rsplit()
    htmlf = htmlt[2]

    htmt = line[8].rsplit()
    htmf = htmt[2]

    txtt = line[9].rsplit()
    txtf = txtt[2]

    pngt = line[10].rsplit()
    pngf = pngt[2]

    gift = line[11].rsplit()
    giff = gift[2]

    jpgt = line[12].rsplit()
    jpgf = jpgt[2]

    jpegt = line[13].rsplit()
    jpegf = jpegt[2]

    csst = line[14].rsplit()
    cssf = csst[2]

    jst = line[15].rsplit()
    jsf = jst[2]

    ict = line[16].rsplit()
    icf = ict[2]

#####-----Finding the type of files supported by the server-----#####
    htmle = htmlt[1]
    htme = htmt[1]
    txte = txtt[1]
    pnge = pngt[1]
    gife = gift[1]
    jpge = jpgt[1]
    jpege = jpegt[1]
    csse = csst[1]
    jse =  jst[1] 
    ice = ict[1]

else:
    print("The ws.conf file is missing. Server cannot be started")
    sys.exit()


if port < 1024:
    print("The port number in ws.conf file is less than 1024.\nPlease change the port number\nTerminating the webserverold")
    sys.exit()

class Server:
#####-----Defining the Server-----#####    
    def __init__(self):
        self.host = ''
        self.port = port
        self.backlg = 5
        self.size = 11024
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
        self.size = 11024

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
                    #print ("\nThis is the decoded request from the the Web Browser: \n" + requestd)
                    requestf = requestd.splitlines()[0]
                    requestf = requestf.rstrip('\r\n')
                    (command, fname, version) = requestf.split()
                    print ("\nCommand is: " + command)
                    print ("\nFile name requested is: " + fname)
                    print ("\nVersion of the request is: " + version)
                    #print (len(fname))
                    cfname = fname.count('/')
                    filename, fileext = os.path.splitext(fname)
                
#####-----Checking for 400 Error-----#####
                    errorcheck400(self, command, cfname, version)
                
#####-----Checking for 501 Error-----#####              
                    errorcheck501(self, fname, fileext)
                
#####-----Getting full path for destination file-----#####                  
                    postpath = str.replace(fname, "/", "\\")
                    fullpath = str(prepath) + str(postpath)
                    print ("\nThe full path of the requested file is: " + fullpath)
                    
#####-----Handling the / or /index.html request-----#####                    
                    if str(fname) == webpf or len(fname) == 1:
                        if os.path.isfile("index.html"):                           
                            fh = open("index.html", "rb")
                            msg = fh.read()
                            fh.close()
                            ct = contype(fname)
                            cl = conlength(fullpath, fname, webpf)
                            responset=header(cl, ct)
                            http_response=(responset+msg)
                    
                        else:
                            print ("file not found")
                            fh = open("http404ep.html", "rb")
                            msg = fh.read()
                            fh.close()
                            cte1 = "text/html".encode()
                            ste1 = os.stat("http404ep.html")
                            cle1 = str(ste1.st_size).encode()
                            http_response = b'HTTP/1.1 404 Not Found\nContent-Type: '+(cte1)+b'\nContent-Length: '+(cle1)+b'\nConnection: Keep Alive\n\n'+msg         
                        self.client.send(http_response)    
                
#####-----Handling the request for other files in root folder-----#####                                      
                    else:
                        if os.path.isfile(fullpath):
                            fh = open(fullpath, "rb")
                            msg = fh.read()
                            fh.close()
                            ct = contype(fname)
                            cl = conlength(fullpath, fname, webpf)
                            responset=header(cl, ct)
                            http_response=(responset+msg)
                                                                                      
                        else:
                            print ("file not found")
                            fh = open("http404ep.html", "rb")
                            msg = fh.read()
                            fh.close()
                            cte1 = "text/html".encode()
                            ste1 = os.stat("http404ep.html")
                            cle1 = str(ste1.st_size).encode()
                            http_response = b'HTTP/1.1 404 Not Found\nContent-Type: '+(cte1)+b'\nContent-Length: '+(cle1)+b'\nConnection: Keep Alive\n\n'+msg
                        self.client.send(http_response)
                        #print(http_response)

                    #request = []
                    #request = self.client.recv(self.size)
                    #request = request
                    request1 = requestd.split("\r\n\r\n")
                    print("\n\nThe splitted request is as per below which is request1: ")
                    print(request1)
                    request2 =[]
                    
#                   i  print(request1[1].encode())
                    if len(request1) > 1: 
                        request2 = request1[1]
                        request2 = str(request2)
                        request2 = request2.encode()
                        print("This is the second request in pipe which is as per below which is request2: ")
                        print(request2)
                        request = []
                        request = request2
                    else:
                        request = []
                    
            except:
                fh = open("http500ep.html", "rb")
                msg = fh.read()
                fh.close()
                cte4 = "text/html".encode()
                ste4 = os.stat("http500ep.html")
                cle4 = str(ste4.st_size).encode()
                http_response = b'HTTP/1.1 500 Internal Server Error\nContent-Type: '+(cte4)+b'\nContent-Length: '+(cle4)+b'\nConnection: Keep Alive\n\n'+msg
                self.client.send(http_response)
                
#####-----Finding the content type of the filename sent in request form ws.config file-----#####                    
def contype(fname):
    filename, fileext = os.path.splitext(fname)
    if fileext == ".html" or len(fname) == 1:
        ct = htmlf
    elif fileext == ".htm":
        ct = htmf    
    elif fileext == ".txt":
        ct = txtf
    elif fileext == ".png":
        ct = pngf
    elif fileext ==".gif":
        ct = giff
    elif fileext == ".jpg":
        ct = jpgf
    elif fileext == ".jpeg":               
        ct = jpegf
    elif fileext == ".css":
        ct = cssf
    elif fileext == ".js":
        ct = jsf
    elif fileext == ".ico":
        ct = icf                
    return ct    

#####-----Finding the content length of the filename sent in request-----#####
def conlength(fullpath, fname, webpf):
    if str(fname) == webpf or len(fname)== 1:
        st = os.stat("index.html")
        cl = st.st_size
    else:   
        st = os.stat(fullpath)
        cl = st.st_size
    return cl
    
#####-----Computing header for each file sent to server-----#####    
def header(cl, ct):
    clf = str(cl).encode()
    ctf = ct.encode()
    responset=b'HTTP/1.1 200 OK\nContent-Type: '+(ctf)+b'\nContent-Length: '+(clf)+b'\nConnection: Keep Alive\n\n'
    #print (responset)
    return (responset)

#####-----Function for Error Code 400: Bad Request-----#####
def errorcheck400(self, command, cfname, version):    
    if command not in ['GET', 'PUT', 'HEAD', 'DELETE'] or cfname > 1 or version != "HTTP/1.1":
        #print ("\n400 error check is working")
        fh = open("http400ep.html", "rb")
        msg = fh.read()
        fh.close()
        cte3 = "text/html".encode()
        ste3 = os.stat("http400ep.html")
        cle3 = str(ste3.st_size).encode()
        http_response = b'HTTP/1.1 400 Bad Request\nContent-Type: '+(cte3)+b'\nContent-Length: '+(cle3)+b'\nConnection: Keep Alive\n\n'+msg
        self.client.send(http_response)
    else: 
        return
        
#####-----Function for Error Code 501: Not Implemented or File Extension not supported-----#####
def errorcheck501(self, fname, fileext):

    if fileext not in [htmle, htme, txte, pnge, gife, jpge, jpege, csse , jse, ice] and len(fname) != 1:
        #print ("\n501 error check is working")
        fh = open("http501ep.html", "rb")
        msg = fh.read()
        fh.close()
        cte2 = "text/html".encode()
        ste2 = os.stat("http501ep.html")
        cle2 = str(ste2.st_size).encode()
        http_response = b'HTTP/1.1 501 Not Implemented\nContent-Type: '+(cte2)+b'\nContent-Length: '+(cle2)+b'\nConnection: Keep Alive\n\n'+msg
        self.client.send(http_response)
    else: 
        return

#####-----Program to call the main code-----#####
if __name__ == "__main__": 
    s = Server() 
    s.run()
    #if SIGINT:
        #SIGKILL()
 
       
    
