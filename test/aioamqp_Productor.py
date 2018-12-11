
#!/usr/bin/env python
"""
    Rabbitmq.com pub/sub example
    https://www.rabbitmq.com/tutorials/tutorial-five-python.html
"""

import asyncio
import aioamqp
import time
import sys


host ='127.0.0.1'
port = 5672
password = 'khb13719208594'
login  = 'guest'

@asyncio.coroutine
def exchange_routing_topic(host,port,login,password):
    try:
        transport, protocol = yield from aioamqp.connect(host,port,login,password)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = yield from protocol.channel()
    exchange_name = 'topic_logs'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

    yield from channel.exchange(exchange_name, 'topic')

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for i in range(10000):
    	yield from channel.publish(message, exchange_name=exchange_name, routing_key='khb')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    yield from protocol.close()
    transport.close()


asyncio.get_event_loop().run_until_complete(exchange_routing_topic(host=host,port=port,login=login,password=password))