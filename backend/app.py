import json
from flask import Flask, jsonify, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal
import pika

# flask db migrate 
# flask db upgrade

# To combine the build frontend with the backend 
# I changed the default static and template folders 
# to fit the Vue output format 
# see Stackoverflow second answer
# https://stackoverflow.com/questions/46214132/how-can-i-combine-vue-js-with-flask
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

# Seting up database                    'postgresql://<username>:<password>@<server>:5432/<db_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/localfinder'

# If set to True (the default) Flask-SQLAlchemy will track modifications of objects and emit signals. 
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Todo %r>' % self.id

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    #task = Test(content="Hallo ich bin ein Beispiel. HALLO")
    try: 
        #db.session.add(task)
        #db.session.commit()
        return jsonify('pong')
    except:
        return 'Faield to commit to the Database. app.route/ping'

@app.route('/api/rabbit', methods=['GET'])
def rabbit():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello Wurlululululu')
    print(' [x] Sent WUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
    connection.close()
    return 'Ich bin ein Hase'

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

if __name__ == '__main__':
    app.run(debug=True)