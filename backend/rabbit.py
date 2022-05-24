import json
import pika
import threading
from flask import Blueprint

exchange = 'microservice.eventbus'
host = 'localhost'

rabbit_route = Blueprint('rabbit_route', __name__)

@rabbit_route.route('/api/rabbit', methods=['GET'])
def rabbit_test():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='local.auth.create')
    msg = '{"name": "Peter","age": 25, "foo": "bar"}'
    channel.basic_publish(exchange='microservice.eventbus', routing_key='local.auth.create', body=msg)
    print(json.dumps(msg))
    connection.close()
    return msg

def reciever_thred():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue='local.auth.status')
    channel.queue_bind(
        exchange='microservice.eventbus', queue='local.auth.status', routing_key="*.#")
    def callback(ch, method, properties, body):
        print(' - Erhalten : %r' % body)
    channel.basic_consume(queue='local.auth.status', on_message_callback=callback, auto_ack=True )
    channel.start_consuming()

reciever = threading.Thread(target=reciever_thred)