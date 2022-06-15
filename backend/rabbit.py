import json
import pika
import threading
from flask import jsonify, make_response, request, Blueprint
from dbModels import Lokal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import dotenv_values

config = dotenv_values(".env")
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
        engine = create_engine(dotenv_values(".env")["DB_FULL_URI"])
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        obj = json.loads(body)
        lok = Lokal(name=obj["localName"], owner=obj["ownerId"])
        session = Session()
        try: 
            session.add(lok)
            session.commit()
        except Exception as e:
            print(e)
            session.close()
            return make_response("ERROR accured. Couldn't create Database Object. In Rabbit!")
        print(' - Erhalten : %r' % obj)
        session.close()
    receive('auth.state', callback) # change to auth.state in production

# Receiver Threads, start in App.py
receiver_local_status = threading.Thread(target=local_status)