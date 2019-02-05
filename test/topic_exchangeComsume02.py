#!/usr/bin/env python
import pika
import sys

username = 'rmqguest01'#指定远程rabbitmq的用户名密码
pwd = '123456'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.106.125.221',credentials=user_pwd))
channel = connection.channel()

queuename = 'test'


channel.exchange_declare(exchange='topic_logs',exchange_type='topic')

result = channel.queue_declare(queue=queuename,durable = True)#durable=True，当消息代理重启该队列依然存在


binding_keys = 'khb.*' #设置绑定键
if not binding_keys:
    print ('not binding_keys')
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queuename,
                       routing_key=binding_key)

print (' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] %r:%r" % (method.routing_key, body,))
    ch.basic_ack(delivery_tag = method.delivery_tag)#处理完数据返回ACK


channel.basic_qos(prefetch_count = 1)#某个消费者忙的时候，不接受消息。
channel.basic_consume(callback,
                      queue=queuename,
                      no_ack=False)

channel.start_consuming()