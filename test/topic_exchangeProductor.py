#!/usr/bin/env python
import pika
import sys
import time
import json


username = 'guest'#指定远程rabbitmq的用户名密码
pwd = 'khb13719208594'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',credentials=user_pwd))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',exchange_type='topic')

routing_key = 'downcmd.routekey' #消息里面只路由键为khb，那么该消息只发送到绑定键存在khb的队列
#message = 'Hello World!'
data = {
		'UUID':'0102030405060708090A0B0C',#设备ID
		'Message':'A11C0102030405060708090A0B0C0304bf9c28f604040000000A5D86',#消息
		'Messageid':'',#随机生成的ID，用于追踪消息状态(成功或不成功)，返回值在status表示
		'status':'' #rabbitmq下发消息状态(1：成功；0：不成功)
}

data1 = {
		'UUID':'0102030405060708090A0B0D',#设备ID
		'Message':'A11C0102030405060708090A0B0C0304bf9c28f604040000000A5D86',#消息
		'Messageid':'',#随机生成的ID，用于追踪消息状态(成功或不成功)，返回值在status表示
		'status':'' #rabbitmq下发消息状态(1：成功；0：不成功)
}

data_list = [data,data1]

while True:
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	for data in data_list:

		Jdata = json.dumps(data)
		try:
			channel.basic_publish(exchange='topic_logs',
			                      routing_key=routing_key,
			                      body=Jdata)
		except Exceptipon as e:
			print(e)
	#print(i)
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	time.sleep(10)
	#print ("[x] Sent %r:%r" % (routing_key, message))
connection.close()