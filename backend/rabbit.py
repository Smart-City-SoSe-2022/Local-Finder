import json
import pika
import threading
import requests
from flask import jsonify, make_response, request, Blueprint
from flask_cors import CORS
from dbModels import Lokal, Account
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import dotenv_values
from jwt_authentication import token_requierd


config = dotenv_values(".env")
credentials = pika.PlainCredentials(config["RABBITMQ_USER"], config["RABBITMQ_PASSWORD"])
exchange = config['EXCHANGE']
host = config['RABBITMQ_URL']

rabbit_bp = Blueprint('rabbit', __name__)

def send(key, queue, body:str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange=exchange, routing_key=key, body=body)
    connection.close()

def receive(key, queue, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.exchange_declare(exchange='microservice.eventbus', exchange_type='topic')
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True )
    channel.start_consuming()

""" Sending route for new location authentication """
@rabbit_bp.route('/api/requestLocal', methods=['POST'])
@token_requierd
def request_local(acc):
    if request.method != 'POST':
        return "Not a POST method"
    body = request.get_json()
    newLocaiton = {
            "ownerId": acc._id,
            "ownerName": acc.name,
            "localName": body['lokalname'],
            "address": body['street'],
            "plz": body['plz'],
            "city": body['city'],
            "accepted": False
    }
    send(key='auth.create', queue=config['QUEUE'], body=json.dumps(body))
    return make_response("Local Auth has been send.")

""" Receiver for answer from Stadtverwaltung """
def local_status():
    def callback(ch, method, properties, body):
        # Setup DB Connection for Thread
        engine = create_engine(dotenv_values(".env")["DB_FULL_URI"])
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        # Loading and adding Object to DB
        obj = json.loads(body)
        lok = Lokal(name=obj["localName"], owner=obj["ownerId"])
        try: 
            session.add(lok)
            session.commit()
        except Exception as e:
            print(e)
            session.close()
            return make_response("ERROR accured. Couldn't create Database Object. In Rabbit!")
        print(' - Erhalten : %r' % obj)
        session.close()
    receive('auth.state', config['QUEUE'], callback)

""" Reciver for Creating Account """
def account_created():
    def callback(ch, method, properties, body):
        # Getting Obj
        obj = json.loads(body)
        print(f"{config['PORTAL_URL']}portal/get/{obj['id']}")
        cookies = {'JWT': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.x1ts3F6kPW4knJoV39M-DG2mEBzcuEVgj7QZBkJIXsc'}
        fAcc = requests.get(f"{config['PORTAL_URL']}portal/get/{obj['id']}", cookies=cookies).json()
        print(fAcc)
        # Setup DB Connection
        engine = create_engine(dotenv_values(".env")["DB_FULL_URI"])
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        #Adding Account
        acc = Account(_id = obj['id'], name = f"{fAcc['forename']} {fAcc['lastname']}", street=fAcc['address'], plz=fAcc['plz'])
        session.add(acc)
        session.commit()
        print(f' - Account angelegt: {acc}')
        session.close()
    receive('portal.account.created', '', callback)

""" Reciver for Deleting Account """
def account_deleted():
    def callback(ch, method, properties, body):
        # Setup DB Connection
        engine = create_engine(dotenv_values(".env")["DB_FULL_URI"])
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        #Deleting Account
        obj = json.loads(body)
        acc = session.query(Account).get(obj['id'])
        if acc:
            session.delete(acc)
            session.commit()
            print(f' - Account gelöscht: {acc}')
        else:
            print("Account konnte nicht gefunden werden.")
        session.close()
    receive('portal.account.deleted', '', callback)


""" Receiver Threads, start in App.py """
receiver_local_status = threading.Thread(target=local_status)
receiver_acc_created = threading.Thread(target=account_created)
receiver_acc_deleted = threading.Thread(target=account_deleted)