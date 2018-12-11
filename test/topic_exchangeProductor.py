#!/usr/bin/env python
import pika
import sys
import time

username = 'guest'#指定远程rabbitmq的用户名密码
pwd = 'khb13719208594'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',credentials=user_pwd))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',exchange_type='topic')

routing_key = 'downcmd.routekey' #消息里面只路由键为khb，那么该消息只发送到绑定键存在khb的队列
message = 'Hello World!'
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
for i in range(1000):
	message = 'Hello World!'+ str(i)
	try:
		channel.basic_publish(exchange='topic_logs',
		                      routing_key=routing_key,
		                      body=message)
	except Exceptipon as e:
		print(e)
#print(i)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#print ("[x] Sent %r:%r" % (routing_key, message))
connection.close()