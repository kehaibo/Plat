import socket
import threading
import sqlite3
import time
from .comm import GlobalValue


lock=threading.Lock()
class TCPClient(threading.Thread):

	def __init__(self,host,port):

		super(TCPClient,self).__init__()

		self.Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		self.revcbuf=b''

		self.host=host

		self.port=port

		self.connmark=False

	def run(self):

		self.StartTCPClient()

		ClientMark=GlobalValue()

		while True:

			if ClientMark.get('connetmark')==True:

				self.Client.send(b'aa')

				ClientMark.del_map('connetmark')

			self.Rec()
			

	def StartTCPClient(self):


		self.Client.settimeout(5)
		self.Client.setblocking(0)

		try:

			self.Client.connect((self.host,self.port))

		except socket.error :

			self.connmark=False

			print("TCP connect fail!!!")

		else:

			self.connmark=True

			print("TCP connect success!!!")


	def Rec(self):

		try:

			self.revcbuf=self.Client.recv(1024)

		except socket.error as e:

			print(e)

def StartClientThread(host,port):

	client=TCPClient(host,port)
	client.setDaemon(False)
	client.start()
	time.sleep(5)
	if client.connmark==True:

		return True

	else:
		return False




