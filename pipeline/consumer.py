import pika

class Consumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def __del__(self):
        self.connection.close()

    def declare_channel(self, name):
        self.channel.queue_declare(queue=name)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        '''
        
        model predict code here.
        
        '''
        print(" Run model predict here. \n")

    def run(self):
        self.channel.basic_consume(
            queue='hello', on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    consumer = Consumer()
    consumer.declare_channel('hello')

    consumer.run()



