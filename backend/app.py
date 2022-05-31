import json
from flask import Flask, jsonify, make_response, render_template, request_started, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal
from rabbit import receiver_local_status, rabbit_route, receiver
from dotenv import dotenv_values

# To combine the frontend-build with the backend,
# I changed the default static and template folders 
#  to fit the Vue output format.
# See Stackoverflow second answer:
# https://stackoverflow.com/questions/46214132/how-can-i-combine-vue-js-with-flask
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.register_blueprint(rabbit_route)
config = dotenv_values(".env.cfg")

""""""""""""""""""""""" 
    Postgre Database 
"""""""""""""""""""""""
# Seting up database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_FULL_URI']

# If set to True (the default) Flask-SQLAlchemy will track modifications of objects and emit signals. 
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

"""""""""""""""""""""""""""""""""""
    Rabbit MQ Lister Threads 
"""""""""""""""""""""""""""""""""""
receiver_local_status.start()
receiver.start()


"""""""""""""""""""""""
    Routing Paths 
"""""""""""""""""""""""

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    try:
        return jsonify('pong')
    except:
        return 'Faield to commit to the Database. app.route/ping'

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

@app.route('/api/createAccount', methods=['POST'])
def create_account():
    if request.method != 'POST':
        return make_response("Request not a POST method")
    body = request.get_json()
    newAcc = Account(name=body["lastname"], street=body["address"], plz=body["plz"])
    try: 
        db.session.add(newAcc)
        db.session.commit()
    except:
        return make_response("ERROR accured. Couldn't create Account")
    return make_response("Account Created")

@app.route('/api/deleteAccount', methods=['DELETE'])
def delete_account():
    if (request.method != 'DELETE'):
        return make_response('Request not a DELETE method')
    body = request.get_json()
    delAcc = db.session.query(Account).get(body["id"])
    if not delAcc:
        return make_response("Account doesn't exist.")
    db.session.delete(delAcc)
    db.session.commit()
    return make_response("Account deletet.")

if __name__ == '__main__':
    app.run(debug=True)