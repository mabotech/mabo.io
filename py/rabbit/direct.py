# -*- coding: utf-8 -*-

"""
heka - rabbitmq - pika
"""

import pika


def callback(ch, method, properties, body):
    #print dir(body)
    #print '\x1e\x03\x08\xbe\x02\x1f'
    print  (body.split("\x1f")[1].strip())
    
def main():    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    """
    channel.exchange_declare(exchange='testout',
                             type='fanout')

    result = channel.queue_declare(queue="hekaq")
    queue_name = result.method.queue
    """
    #channel.queue_declare(queue="hekaq")
    channel.queue_bind(exchange='heka',
                       queue="hekaq")

    print ' [*] Waiting for logs. To exit press CTRL+C'



    channel.basic_consume(callback,
                          queue="hekaq",
                          no_ack=True)

    try:
        channel.start_consuming()
    except:
        pass
    
if __name__ == '__main__':
    main()        