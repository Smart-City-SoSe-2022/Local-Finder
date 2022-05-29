import json
import pika
import threading
from flask import Flask, jsonify, make_response, render_template, request_started, url_for, request, Blueprint
from dbModels import db, Lokal
from dotenv import dotenv_values

config = dotenv_values(".env.cfg")
for x in config:
    print(x)

exchange = config['EXCHANGE']
queue = config['QUEUE']
host = config['HOST']

rabbit_route = Blueprint('rabbit_route', __name__)

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
@rabbit_route.route('/api/requestLocal', methods=['POST'])
def request_local():
    if request.method != 'POST':
        return "Not a POST method"
    body = request.get_json()
    send(key='auth.create', body=json.dumps(body))
    return make_response("ok")

# Receiver for answer from Stadtverwaltung
def local_status():
    def callback(ch, method, properties, body):
        
        lok = Lokal(owner=body.ownerId)
        try: 
            db.session.add(lok)
            db.session.commit()
        except: 
            return "Fehler: Account konnte nicht angelegt werden..."
        print(' - Erhalten : %r' % body)
    receive('auth.status', callback)

# Test route for rabbitMQ
@rabbit_route.route('/api/rabbit', methods=['GET'])
def rabbit_test():
    msg = '{"name": "Peter","age": 25, "foo": "bar"}'
    send('hallo', msg)
    print(json.dumps(msg))
    return msg

# Test listener for rabbitMQ
def test_reviever():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.queue_bind(
        exchange='microservice.eventbus', queue=queue, routing_key="*.#")
    def callback(ch, method, properties, body):
        print(' - Erhalten : %r' % body)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True )
    channel.start_consuming()

# Receiver Threads, start in App.py
receiver = threading.Thread(target=test_reviever)
receiver_local_status = threading.Thread(target=local_status)