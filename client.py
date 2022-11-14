#!/bin/python3
import socket
import argparse
import sys
import random as rnd
import time

header = 64
format = 'utf-8'
disconnect_msg = 'DISCONNECT'




LETTERS="abcdifghijklmnopqrstuvwxyz"

aparse = argparse.ArgumentParser("This is small test client application for K8s tests. Witch send some data on TCP port and address and get answers.")
aparse.add_argument( "--port", type=int, required=True, help="TCP port for connecting")
aparse.add_argument( "--address", type=str, required=True, help="Address for connecting.")
aparse.add_argument( "--sleep", type=int, required=False, help="Sleep timer in seconds. No sleep by default.")

args = aparse.parse_args()

address = args.address
port = args.port
slp = args.sleep

def data_processor(data):
	#do somting with data
	return data

def gen_message(n):
    out = ''
    for i in range(n):
        if rnd.choice([0,1]):
            out = out + LETTERS[rnd.randrange(len(LETTERS))].upper()
        else:
            out = out + LETTERS[rnd.randrange(len(LETTERS))].lower() 
    return out



def send_msg(msg):
	msg_len = str(len(msg)).encode(format)
	msg_len += b' ' * (header - len(msg_len))
	client.send(msg_len)
	client.send(msg.encode(format))
	print(client.recv(2048).decode(format))



try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((address, port))


	while True:
		send_msg(gen_message(32))
		if slp:
			time.sleep(slp)

except KeyboardInterrupt:
	send_msg(disconnect_msg)
	client.close()
	sys.exit(0)
except Exception as exc:
	send_msg(disconnect_msg)
	client.close()
	print( "Error : ", exc)
	sys.exit(1)
