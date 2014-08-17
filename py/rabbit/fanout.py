# -*- coding: utf-8 -*-

"""
heka - rabbitmq - pika
"""


import pika


def callback(ch, method, properties, body):
    #print "%r" % (body)
    print  (body.split("\x1f")[1].strip())
    
def main():    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    """
    channel.exchange_declare(exchange='testout',
                             type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    """
    result = channel.queue_declare(queue="mabo")
    
    channel.queue_bind(exchange='testout',
                       queue="mabo")

    print ' [*] Waiting for logs. To exit press CTRL+C'



    channel.basic_consume(callback,
                          queue="mabo",
                          no_ack=True)
    
    try:
        channel.start_consuming()
    except:
        pass
    
if __name__ == '__main__':
    main()        