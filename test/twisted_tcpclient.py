#TCPClient

from twisted.internet import reactor,protocol
import time
import array
import struct

tran_Copy={}
connectedMark=0
class EchoClient(protocol.Protocol):

	def __init__(self):

		self.temp_cmd='A11C0102030405060708090A0B0D0304bf9c28f604040000000A5F07'
		self.send_cmdbyte=b''

	def connectionMade(self):
		global connectedMark
		cmd_array=bytearray.fromhex(self.temp_cmd.upper())
		for i in cmd_array:
			self.send_cmdbyte=self.send_cmdbyte+struct.pack('B',i)
		tran_Copy['trans']=self.transport
		connectedMark=1
		#self.transport.write(self.send_cmdbyte)
		send_data(tran_Copy['trans'],self.send_cmdbyte)
		print('connected ok!'+str(tran_Copy['trans']))

	def dataReceived(self,data):

	    print('Server said:'+str(data.decode('utf-8')))
	    self.transport.loseConnection()

	def connectionLost(self,reason):

	    print('connection lost!!!')

class EchoClienFactory(protocol.ClientFactory):

	def buildProtocol(self,addr):

	    return EchoClient()

	def startedConnecting(self, connector):

	    print('started connect!!!')

	def clientConnectionFailed(self, connector, reason):

	    print('client Connection Failed!!!')

	    reactor.stop()

	def clientConnectionLost(self, connector, reason):

	    print('client Connection Lost!!!')

	    print(reason)

	    reactor.stop()

def send_data(transport,data):

	reactor.callLater(10,send_data,tran_Copy['trans'],data)
	transport.write(data)
	#print("send ok! at{}\n".format(time.strftime(" %Y-%m-%d %H:%M:%S",time.localtime())))
	#   整体数据长度+数据长度类型（固定长度与不定长度）+设备类型标识+数据类型标识+数据+crc校验：0x07 0xxx 0xxx 0x00 0x00 0x01 0x10 0xxx 0xxx 
	#   发送tmep 指令： 0x07 0xFF 0x01 0xA0 0x00 0x00 0x00 0x01 40 75   0xff：代表固定长度的指令 0xFE代表不定长度的指令
	#   对应数据长度不定的指令，单独使用一个标识，固定长度的指令使用不一样的标识

reactor.connectTCP('47.106.125.221',8001,EchoClienFactory())
#reactor.connectTCP('192.168.0.133',8001,EchoClienFactory())

reactor.run()



