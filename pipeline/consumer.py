import pika

from predictor import Predictor
import time
import os

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
        write to csv
        
        '''
        predictor = Predictor()

        face_img_path = body
        if not os.path.exists(face_img_path):
            print("face path not exist.")
            return

        img_name = str(body).split('\\')[-1]
        # print(img_name)
        with open(face_img_path, 'rb') as f:
            image_bytes = f.read()

            print("inference:")
            start_time = time.time()
            label = predictor.predict(image_bytes, img_name)
            end_time = time.time()
            inference_latency = end_time - start_time
            print("label = " + str(label) + ", " + str(inference_latency))


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



