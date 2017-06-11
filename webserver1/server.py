#!/usr/env python

# Author :Vihanga Bare #

import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 
import sys
import sqlite3
from sqlite3 import Error
import json
from pprint import pprint 

# Open the socket and initialise the server #
TCP_IP = '127.0.0.1' 
TCP_PORT = 8888 
BUFFER_SIZE = 1024 #maximum size of the buffer

with open('data.json', 'r') as f:
    json_data = json.load(f)
    print("server side json ")
    pprint(json_data)

sql_create_data_table = """CREATE TABLE IF NOT EXISTS data (
				id integer PRIMARY KEY, 
				name text NOT NULL, 
				date text NOT NULL);"""   
    
sql_insert_value = """INSERT INTO data (
			id,
			name,
			date) 
			VALUES (
			?,
                        ?,
                        ?);"""
    
sql_del_value = """DELETE 
                      FROM 
                      data 
                      WHERE 
                      name = ?;"""

sql_disp_value = """SELECT * FROM data ORDER BY id;"""

sql_updt_value = """UPDATE data
			SET name = ?
			WHERE 
			 id = ?;"""


# New thread created for evry connection #
class RequestThread(Thread): 
 
    def __init__(self,ip,port,connection): 
        Thread.__init__(self) 
        self.connection = connection
	self.ip = ip 
        self.port = port 
	#self.conn = conn
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
 
    def run(self): 
        while True : 
            data = self.connection.recv(1024) 
            print "Server received data:", data
            MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            self.connection.send(MESSAGE)  # echo 
	    database_tasks(data) 
 
class Server:
    def __init__(self):
	self.host =TCP_IP
        self.port =TCP_PORT
	self.size = 1024
	self.server = None
        self.threads = []
     
    def open_socket(self):
	try:
	    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    self.server.bind((self.host, self.port))
	except socket.error as e:
	    if self.server:
		self.server.close() 
	    print("Socket Error:"+e.message)
	    sys.exit(1)

    def run(self):
	self.open_socket()
	while True: 
	    self.server.listen(600)
    	    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    	    (connection, (ip,port)) = self.server.accept() 
    	    newthread = RequestThread(ip,port,connection) 
    	    newthread.start() 
            self.threads.append(newthread) 
 
	self.server.close()
	for t in self.threads: 
            t.join() 
 
 
def create_connection(db_file):
    # create a database connection to a SQLite database 
    # and return the connection object #
    try:
        conn = sqlite3.connect(db_file)
        print "Connection created : "+ sqlite3.version
	return conn

    except Error as e:
        print("Error in create_connection : " + e.message)

    return None

def create_table(connect,create_table_sql):
    # create a table by create table sql statement #
    try:
	c = connect.cursor()
	c.execute(create_table_sql)
        connect.commit()
	
    except Error as e:
	print("Error in create_table :" + e.message)

def insert_values(connect,sql_insert_value):
    # insert values into table by sql statement #
    try:
	c = connect.cursor()
	c.execute(sql_insert_value,(json_data["data"][0]["id"],json_data["data"][0]["name"],json_data["data"][0]["date"]))
        connect.commit()
	
    except Error as e:
	print("Error in insert_values :" + e.message)


def delete_values(connect,sql_del_value):
    # insert values into table by sql statement #
    try:
	c = connect.cursor()
	c.execute(sql_del_value,(json_data["data"][1]["name"],))
        connect.commit()
	
    except Error as e:
	print("Error in delete_values :" + e.message)

def display_values(connect,sql_disp_value):
    # display values into table by sql statement #
    try:
	c = connect.cursor()
	for row in c.execute(sql_disp_value):
	    print row
        connect.commit()
	
    except Error as e:
	print("Error in display_values :" + e.message)

def update_values(connect,sql_updt_value):
    # update values into table by sql statement #
    try:
	c = connect.cursor()
	c.execute(sql_updt_value,(json_data["data"][1]["name"],json_data["data"][1]["id"]))
        connect.commit()
	
    except Error as e:
	print("Error in display_values :" + e.message)

def database_tasks(message):
    try:
	database = 'pythonsqlite.db'
    	# create database connection #
    	conn = create_connection(database)

    	if conn is not None:
    	
        #create_table(conn,sql_create_data_table)
	#insert_values(conn,sql_insert_value)
        #delete_values(conn,sql_del_value)
        #display_values(conn,sql_disp_value)
        #update_values(conn,sql_updt_value)
        #s = Server()
        #s.run(conn)
	    if message == 'create':
	        create_table(conn,sql_create_data_table)

            elif message == 'insert':
	        insert_values(conn,sql_insert_value)

            elif message == 'update':
                update_values(conn,sql_updt_value)

            elif message == 'delete':
                delete_values(conn,sql_del_value)

	    elif message == 'display':
		display_values(conn,sql_disp_value)

            else:
		print("enter insert,update,delete,display as commands")
        else:
            print("Error! cannot create database connection")
    except:
        print("error")

def Main():
    s = Server()
    s.run()

if __name__ == "__main__":
   Main()	
