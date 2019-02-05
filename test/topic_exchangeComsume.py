#!/usr/bin/env python
import pika
import sys

username = 'guest'#指定远程rabbitmq的用户名密码
pwd = 'khb13719208594'
user_pwd = pika.PlainCredentials(username, pwd)
parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=user_pwd)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

#queuename = 'khb1'
queuename = 'celery'


channel.exchange_declare(exchange='celery',exchange_type='direct')

result = channel.queue_declare(queue=queuename)#durable=True，当消息代理重启该队列依然存在


#binding_keys = 'khb1' #设置绑定键
'''if not binding_keys:
    print ('not binding_keys')
    sys.exit(1)
    '''

#channel.queue_bind(exchange='celery',queue=queuename,routing_key=binding_keys)
channel.queue_bind(exchange='celery',queue=queuename)

print (' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] %r:%r" % (method.routing_key, body,))
    ch.basic_ack(delivery_tag = method.delivery_tag)#处理完数据返回ACK


channel.basic_qos(prefetch_count = 1)#某个消费者忙的时候，不接受消息。
channel.basic_consume(callback,
                      queue=queuename,
                      no_ack=False)

channel.start_consuming()

#print(d)