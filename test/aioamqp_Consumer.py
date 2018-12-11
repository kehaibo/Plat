#!/usr/bin/env python
"""
    Rabbitmq.com pub/sub example
    https://www.rabbitmq.com/tutorials/tutorial-five-python.html
"""

import asyncio
import aioamqp

import random
import sys
import time

host ='127.0.0.1'
port = 5672
password = 'khb13719208594'
login  = 'guest'

@asyncio.coroutine
def callback(channel, body, envelope, properties):
    print("consumer {} received {} ({})".format(envelope.consumer_tag, body, envelope.delivery_tag))
    #body = body
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


@asyncio.coroutine
def receive_log(host,port,login,password):
    try:
        transport, protocol = yield from aioamqp.connect(host,port,login,password)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = yield from protocol.channel()
    exchange_name = 'topic_logs'

    yield from channel.exchange(exchange_name, 'topic')

    result = yield from channel.queue(queue_name='khb', durable=False, auto_delete=True)

    binding_keys = 'khb.*' 

    for binding_key in binding_keys:
        yield from channel.queue_bind(
            exchange_name='topic_logs',
            queue_name='khb',
            routing_key=binding_key
        )

    #print(' [*] Waiting for logs. To exit press CTRL+C')
    for i in range(100):
        yield from channel.basic_consume(callback, queue_name='khb',no_ack =True)

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(receive_log(host,port,login,password))
event_loop.run_forever()