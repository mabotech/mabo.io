#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  """

import socket
import gevent

import pika

import uuid

class FibonacciRpcClient(object):
    
    """ rpc client """
    def __init__(self):
        """ init """

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """ response """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        """ call """
        
        self.response = None
        
        self.corr_id = str(uuid.uuid4())
        print self.corr_id
        
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
                                   
        while self.response is None:
            self.connection.process_data_events()
            
        return int(self.response)


def main():
    
    """ main """
    
    fibonacci_rpc = FibonacciRpcClient()

    for i in xrange(1,200):
        
        j = i % 20
        
        print " [x] Requesting fib(%s)" % (j)
        
        response = fibonacci_rpc.call(j)
        
        print " [.] Got %r" % (response,)
        
        gevent.sleep(1)
    
    
if __name__ == '__main__':
    main()    