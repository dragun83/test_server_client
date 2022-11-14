#!/usr/local/bin/python3

import socket
import argparse
import sys
import threading
import time

#config
def_port=30000 		#default port
def_addr=''		#default listener address (empty for all interfaces)
head = 64		#bytes of header message
format = 'utf-8'	#message format
disconnect_msg = 'DISCONNECT'	#disconnect signal

#create arguments

aparse = argparse.ArgumentParser("This is small test server application for K8s tests. Witch catch some data on TCP port and do someting.")
aparse.add_argument( "--port", type=int, required=False, help="TCP port for listening. Default 30000")
aparse.add_argument( "--listen", type=str, required=False, help="Address for listening on. If emty listening on all interfaces.")
args = aparse.parse_args()

interface = args.listen
port = args.port

if interface is None:
	interface = def_addr
if port is None:
	port = def_port

# define some functions

def client_serv(conn, addr):
	print(" Client address : ", addr, " connected at : ", time.asctime())
	connected = True
	while connected:
		msg_length = conn.recv(head).decode(format)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(format)
			if msg == disconnect_msg:
				connected = False
			print(f"[{addr}] {msg}")
			answer = (f"I recieve from {addr} at {time.asctime()} this shit: {msg}")
			conn.send(answer.encode(format))
	conn.close()

def init_srv():
	server.listen()
	print("Server started!")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target= client_serv, args=(conn, addr))
		thread.start()
		print(f"Active connections : {threading.activeCount() - 1}")
# start main programm
try:

	print ("Staring server...")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((interface, port))
	init_srv()

except KeyboardInterrupt:
	server.close()
	print("Interrupted by keyboard")
	sys.exit(0)
except Exception as exp:
	server.close()
	print("Error : ", exp)
	sys.exit(1)
