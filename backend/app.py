import json
import threading
from flask import Flask, jsonify, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal
import pika

# flask db migrate 
# flask db upgrade

# To combine the frontend-build with the backend,
# I changed the default static and template folders 
#  to fit the Vue output format.
# See Stackoverflow second answer:
# https://stackoverflow.com/questions/46214132/how-can-i-combine-vue-js-with-flask
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

### Postgre Database

# Seting up database connection         'postgresql://<username>:<password>@<server>:5432/<db_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/localfinder'

# If set to True (the default) Flask-SQLAlchemy will track modifications of objects and emit signals. 
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

### Rabbit MQ


##### Routing Paths #####

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    try: 
        return jsonify('pong')
    except:
        return 'Faield to commit to the Database. app.route/ping'

@app.route('/api/newAccount')
def new_account():
    name = request.args.get('name')
    print(name)
    age = request.args.get('age')
    print(age)
    acc = Account(name=name, age=age)
    try: 
        db.session.add(acc)
        db.session.commit()
    except: 
        return "Fehler: Account konnte nicht angelegt werden..."
    return name + " erfolgreich angelegt!"

@app.route('/api/getAccounts')
def get_accounts():
    # Account.query.filter_by(name="Peter").first()
    accs = db.session.query(Account)
    if accs:
        print(accs.all())
        return "Printed in Server Log"
    else:
        return "No accounts found"


##### Rabbit MQ Fuctions #####

@app.route('/api/rabbit', methods=['GET'])
def rabbit():
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
reciever.start()

if __name__ == '__main__':
    app.run(debug=True)