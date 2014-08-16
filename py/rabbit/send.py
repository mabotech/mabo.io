# -*- coding: utf-8 -*-

"""  """

import socket
import gevent

import pika

import random

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
                   
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    
    while True:
    
        r = random.random()
        
        msg = "msg:%s" % (r)
        
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=msg)
                              
        print msg
        
        gevent.sleep(r)
        
    connection.close()
    
if __name__ == '__main__':
    main()    