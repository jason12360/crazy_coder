import signal
import time
import os
from socket import *
import sys
def run(parent_pid,_recv_queue,_send_queue):
	HOST = '127.0.0.1'
	PORT = 18529
	global ADDR
	ADDR = (HOST, PORT)
	global s
	s = socket(AF_INET, SOCK_DGRAM)

	signal.signal(41,get_chat)
	global send_queue
	global recv_queue
	send_queue = _send_queue
	recv_queue = _recv_queue
	while True:
		msg, addr = s.recvfrom(1024)
		recv_queue.put(msg.decode())
		os.kill(parent_pid,40)


def get_chat(sig,frame):
	msg = send_queue.get()
	s.sendto(msg.encode(),ADDR)



