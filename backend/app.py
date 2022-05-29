import json
from flask import Flask, jsonify, render_template, request_started, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal
from rabbit import receiver_local_status, rabbit_route, receiver
from dotenv import dotenv_values

config = dotenv_values(".env.cfg")
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
app.register_blueprint(rabbit_route)

### Postgre Database

# Seting up database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_FULL_URI']

# If set to True (the default) Flask-SQLAlchemy will track modifications of objects and emit signals. 
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

### Rabbit MQ
receiver_local_status.start()
receiver.start()
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

# @app.route('/api/newAccount')
# def new_account():
#     name = request.args.get('name')
#     print(name)
#     age = request.args.get('age')
#     print(age)
#     acc = Account(name=name, age=age)
#     try: 
#         db.session.add(acc)
#         db.session.commit()
#     except: 
#         return "Fehler: Account konnte nicht angelegt werden..."
#     return name + " erfolgreich angelegt!"

# @app.route('/api/getAccounts')
# def get_accounts():
#     # Account.query.filter_by(name="Peter").first()
#     accs = db.session.query(Account)
#     if accs:
#         print(accs.all())
#         return "Printed in Server Log"
#     else:
#         return "No accounts found"

@app.route('/api/search')
def search_request():
    #destination = request.args.get('destination')
    pass

@app.route('/api/downloadFile')
def download_file():
    #file = request.args.get('file')
    pass

@app.route('/api/requestReservation')
def request_reservation():
    pass

if __name__ == '__main__':
    app.run(debug=True)