import pika
import threading
from app import app

@app.route('/api/rabbit', methods=['GET'])
def rabbit_test():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='microservice.eventbus', routing_key='localfinder.rabbit', body='Hello Wurlulu')
    print(' [x] Sent WUU')
    connection.close()
    return 'Ich bin ein Hase'


### Defining the reciever thread
def reciever_thred():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    def callback(ch, method, properties, body):
        print(' iks) Erhalten %r' % body)
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True )
    channel.start_consuming()

reciever = threading.Thread(target=reciever_thred)