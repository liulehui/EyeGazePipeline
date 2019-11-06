import pika

class Publisher:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
    def __del__(self):
        self.connection.close()

    def declare_queue(self, name):
        self.channel.queue_declare(queue=name)

    def publish(self, body):
        self.channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=body)
        print(" [x] Sent '" + str(body) + "'")






