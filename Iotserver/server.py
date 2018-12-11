#TCPSerever
#-*- coding:utf-8 -*-
import os
if os.name =='nt':
	from twisted.internet import iocpreactor
	iocpreactor.install()
from twisted.internet import reactor,protocol,task,defer
from pika.adapters import twisted_connection
from twisted.internet.error import ConnectionDone
from AutodelectProtocol.Autodelectprotoctol import AutoDelect,AutoDelectSuccess,AutoDelectFail
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.enterprise import adbapi
from comm.comm import loglocal
from sys import argv
import binascii
from CRC16.CRC16 import CRC16_1
import time
import datetime
import queue
import pymysql
import sys
import pika

log.startLogging(DailyLogFile.fromFullPath(loglocal))
"""上报数据解析流程：
A0 16 01 02 03 04 05 06 07 08 09 0A 0B 0C 01 04 00 0B 0A 01 F2 60

1、获取数据模型
	按照uuid获取模型

2、获取模型对应的值
model_struct = {
	'model_name':'khb_product_1',
	'data_type' : {
				'A0':{'02':'Float','03':'Float'},
				'A1':{'03':'Float','04':'UInt'} 
	}
	'updata_procotol':....,
	....
}'
3、解析数据
实现：
def hanlder(data):
	pass
"""	

class Echo(protocol.Protocol):#处理事件程序

	def __init__(self,factory):
		''' 初始化'''
		self.factory = factory
		self.factory.devices[self] = self
		self.heartbeat_time = self.factory.heartbeat_time
		self.lastheartbeat_time = datetime.datetime.now()
		self.model_struct = {
				'model_name':'',
				'data_type':dict(),
				'typemappointname':dict(),#数据点type与数据点name键值对，用于插入数据到设备数据表
		}
		self.UUID = ''
		self.devicestatus  = '0'#设备状态 0：离线 1：设备被迫离线 2：在线
		self.statusmapinfo = '自动下线'

	def dataReceived(self,data):
		''' 重写数据接收函数'''
		self.datahanlder(data)
		
		
	def datahanlder(self,data):
		'''数据处理方法'''
		#print(data)
		datastr=binascii.hexlify(data).decode('utf-8').upper()#16进制字符串
		#log.msg('info:{}\n'.format(datastr))
		if CRC16_1(data):#crc检验
			self.UUID= datastr[4:28]	
			if ((datetime.datetime.now()-self.lastheartbeat_time).seconds <= self.heartbeat_time):
				self.hreatbeattimeout.reset(self.heartbeat_time)

			if self.devicestatus != '2':
				self.devicestatus = '2'
				self.statusmapinfo = '设备上线'
				self.execute_device_status(self.devicestatus,self.statusmapinfo)

			if self.model_struct['model_name']:
				'''模型名字存在则不需要获取，反之，获取模型。'''
				defer_instancs = AutoDelect(self.model_struct,datastr,sqlconnect)
				defer_instancs.addCallback(AutoDelectSuccess)
				defer_instancs.addErrback(AutoDelectFail)
			else:
				cur=sqlconnect.runInteraction(self.get_model_id,self.UUID)
				cur.addErrback(self.sql_error)
				cur.addCallback(self.execute_get_type,datastr)
		else:
			self.devicestatus = '1'
			self.statusmapinfo = 'CRC ERROR'
			self.transport.abortConnection()
			log.msg('error:CRC ERROR')	
		self.lastheartbeat_time = datetime.datetime.now()


	
	def SEND(self,uuid,databody):

		pass



	def connectionLost(self, reason):
		"""
		Called when the connection is shut down.

		Clear any circular references here, and any external references
		to this Pr  otocol.  The connection has been closed.

		@type reason: L{twisted.python.failure.Failure}
		"""
		if reason.type==ConnectionDone:#该类可判断设备为主动断开
			self.devicestatus = 0
			self.statusmapinfo = '自动下线'
		self.factory.ConnectNum = self.factory.ConnectNum - 1
		self.hreatbeattimeout.cancel()
		self.execute_device_status(self.devicestatus,self.statusmapinfo)
		log.msg("info:{} disconnected".format(self.UUID))    
	
	def connectionMade(self):
		self.factory.ConnectNum = self.factory.ConnectNum + 1
		if self.factory.ConnetNum_Max < self.factory.ConnectNum:
			self.factory.ConnetNum_Max = self.factory.ConnectNum
		else:
			self.factory.ConnectLost_Num = self.factory.ConnetNum_Max - self.factory.ConnectNum
		
		self.hreatbeattimeout = reactor.callLater(self.heartbeat_time,self.hearttimeout_handler)#心跳检测

	def get_model_id(self,cursor,UUID):
		''' 通过UUID查询数据模型id'''
		query_model_id = "select model_name_id from decive_deviceinfo where UUID = '{}'".format(UUID) 
		cursor.execute(query_model_id)
		model_id=cursor.fetchall()[0]
		return model_id

	def execute_get_type(self,model_id,datastr):
		_stream_type=sqlconnect.runInteraction(self.get_stream_type,model_id[0])
		_stream_type.addErrback(self.sql_error)
		_stream_type.addCallback(self.execute_get_pointtype,datastr)

	def get_stream_type(self,cursor,model_id):
		'''获取数据流类型'''
		query_stream_type= "SELECT decive_productmodelname.product_model,decive_stream.stream_Type,decive_stream.id from  decive_productmodelname right join  decive_stream on decive_productmodelname.id=decive_stream.model_name_id and decive_productmodelname.id={}".format(model_id) 
		cursor.execute(query_stream_type)
		model_streamtype=cursor.fetchall()
		data_typedict={}
		self.model_struct['model_name'] = model_streamtype[0][0]
		for stream_type in model_streamtype:
			 data_typedict[stream_type[1]] = ''
		self.model_struct['data_type'] = data_typedict
		#print(self.model_struct)
		del data_typedict
		return model_streamtype

	def execute_get_pointtype(self,model_streamtype,datastr):
		#log.msg(model_streamtype)
		_point_type=sqlconnect.runInteraction(self.get_point_type,model_streamtype)
		_point_type.addErrback(self.sql_error)
		_point_type.addCallback(self.get_model_struct,datastr)

	def get_point_type(self,cursor,model_streamtype):
		'''获取数据点类型'''
		point_typelist = list()
		for m in model_streamtype:
			query_point_type= "SELECT decive_data_point.TLV_Type,decive_data_point.data_type,decive_data_point.data_name FROM decive_data_point RIGHT JOIN  decive_stream_point ON decive_stream_point.data_point_id = decive_data_point.id and decive_stream_point.stream_id='{}' WHERE  decive_data_point.data_type is not null".format(m[2]) 
			cursor.execute(query_point_type)
			point_types=cursor.fetchall()
			point_typelist.append(point_types)
		return point_typelist

	def get_model_struct(self,point_typelist,datastr):
		index=0
		for key,value in self.model_struct['data_type'].items():
			type_dict = dict()
			name_dict = dict()
			for tupleindex in range(len(point_typelist[index])):
				type_dict[point_typelist[index][tupleindex][0]] = point_typelist[index][tupleindex][1]
				name_dict[point_typelist[index][tupleindex][0]] = point_typelist[index][tupleindex][2]
			self.model_struct['data_type'][key]=type_dict
			self.model_struct['typemappointname'][key] = name_dict
			index =index + 1 
		defer_instancs = AutoDelect(self.model_struct,datastr,sqlconnect)
		defer_instancs.addCallback(AutoDelectSuccess)
		defer_instancs.addErrback(AutoDelectFail)
		#log.msg(self.model_struct) 

	def execute_device_status(self,status,info):
		_device_status=sqlconnect.runInteraction(self.insert_device_status,status,info)
		_device_status.addErrback(self.sql_error)

	def insert_device_status(self,cursor,status,info):
		'''插入设备状态及信息'''
		currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		insert_status_sql = "INSERT INTO decive_devicestatus (UUID,status,info,currenttime) VALUES ('{}','{}','{}','{}');".format(self.UUID,status,info,currenttime)
		cursor.execute(insert_status_sql)

	def sql_error(self,err):
		log.err('error:{}'.format(err.getErrorMessage()))
	
	def hearttimeout_handler(self):
		''' 心跳超时超时处理'''
		self.devicestatus = '1'
		self.statusmapinfo = '心跳超时'
		self.transport.abortConnection()
		log.msg('info:{} timeout'.format(self.UUID))


class EchoFactory(protocol.Factory):

	def __init__(self):
		self.devices = {}
		self.ConnectNum=0
		self.ConnetNum_Max=0
		self.ConnetLost_Num=0
		self.heartbeat_time=60 #心跳超时

	def buildProtocol(self, addr):  #重写该函数，该函数返回protocol的实例

		return Echo(self)


class RabbitMQ(object):
	'''rabbitmq class'''
	_connection = None
	_channel = None

	host = 'localhost'
	port = 5672
	username = 'guest'
	password = 'khb13719208594'

	queuename = 'downcmd'
	binding_keys = 'downcmd.routekey' 
	

	@staticmethod
	@defer.inlineCallbacks
	def init_mq():
		credentials = pika.PlainCredentials(RabbitMQ.username,RabbitMQ.password)
		parameters = pika.ConnectionParameters(credentials=credentials)
		cc = protocol.ClientCreator(reactor,twisted_connection.TwistedProtocolConnection,parameters)
		RabbitMQ._connection = yield cc.connectTCP(host=RabbitMQ.host,port=RabbitMQ.port)
		defer.returnValue(1)

	@staticmethod
	@defer.inlineCallbacks
	def set_channel_receive_from_back():
		"""
		设置rabbitmq消息接受队列的channel，并且做好循环任务
		"""
		RabbitMQ._channel= yield RabbitMQ._connection.channel()
		yield RabbitMQ._channel.exchange_declare(exchange='topic_logs',exchange_type='topic')
		yield RabbitMQ._channel.queue_declare(queue=RabbitMQ.queuename)
		yield RabbitMQ._channel.queue_bind(exchange='topic_logs', queue=RabbitMQ.queuename, routing_key=RabbitMQ.binding_keys)
		
		'''默认启动10个消费者'''
		for i in range(10):
			queue_object,tag = yield RabbitMQ._channel.basic_consume(queue=RabbitMQ.queuename, no_ack=True)
			l = task.LoopingCall(RabbitMQ.read_from_mq, queue_object)
			l.start(0.2)
		defer.returnValue(1)

	@staticmethod
	@defer.inlineCallbacks
	def read_from_mq(queue_object):
		"""
		读取接受到的消息队列消息，并且处理
		"""
		ch, method, properties, body = yield queue_object.get()

		if body:
		    #log.msg('Accept data from http successful!')
		    #chat_factory.process_data_from_mq(body)
		    print (" [x] %r:%r" % (method.routing_key, body,))
		    defer.returnValue(1)
		defer.returnValue(0)

	@staticmethod
	def rmqerror(err):
		log.msg('rabbitmqerr:'+str(err.getErrorMessage()))   

if __name__ == '__main__':

	mysqlsetting =	{   'host':'47.106.125.221',
						'port':3306,
						'user':'root',
						'passwd':'123456',
						'db':'django',
						'use_unicode':True,
						'charset':'utf8'
					}

	try:
		sqlconnect = adbapi.ConnectionPool("pymysql",**mysqlsetting) 
	except Exception as e:
		log.msg('error:{}'.format(e))

	reactor.callLater(0.1,RabbitMQ.init_mq)
	reactor.callLater(0.5,RabbitMQ.set_channel_receive_from_back)

	Devfactory=EchoFactory()

	reactor.listenTCP(8002,Devfactory)
	
	print("Listening....\n")

	reactor.run()
	
	
