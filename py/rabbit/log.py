import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    
    try:
        channel.exchange_declare(exchange='testout',
                                 type='fanout')
    except pika.exceptions.ChannelClosed as cc:
        print cc
        #raise
        
    result = channel.queue_declare(queue="mabo")
    queue_name = result.method.queue
    print queue_name
    channel.queue_bind(exchange='testout',
                       queue=queue_name)

    print ' [*] Waiting for testout. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print " [x] %r" % (body,)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
    
   
if __name__ == '__main__':
    main()    