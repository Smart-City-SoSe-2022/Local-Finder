import json
import pika
import threading
from flask import jsonify, make_response, request, Blueprint
from dbModels import Lokal, addObj
from dotenv import dotenv_values

config = dotenv_values(".env.cfg")
exchange = config['EXCHANGE']
queue = config['QUEUE']
host = config['HOST']

rabbit_bp = Blueprint('rabbit', __name__)

def send(key, body:str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange=exchange, routing_key=key, body=body)
    connection.close()

def receive(key, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.exchange_declare(exchange='microservice.eventbus', exchange_type='topic')
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True )
    channel.start_consuming()

# Sending route for new location authentication
@rabbit_bp.route('/api/requestLocal', methods=['POST'])
def request_local():
    if request.method != 'POST':
        return "Not a POST method"
    body = request.get_json()
    send(key='auth.create', body=json.dumps(body))
    return make_response("Local Auth has been send.")

# Receiver for answer from Stadtverwaltung
def local_status():
    def callback(ch, method, properties, body):
        obj = json.loads(body)
        lok = Lokal(name=obj["localName"], owner=obj["ownerId"])
        addObj(lok)
        print(' - Erhalten : %r' % obj)
    receive('auth.status', callback)

# Receiver Threads, start in App.py
receiver_local_status = threading.Thread(target=local_status)