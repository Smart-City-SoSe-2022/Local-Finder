from flask import Flask, jsonify, make_response, render_template, request_started, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from rabbit import rabbit_bp, receiver_local_status
from flask_migrate import Migrate
from datetime import datetime
from dbModels import Account, Reservation, Lokal, addObj, db
from dotenv import dotenv_values

# To combine the frontend-build with the backend,
# I changed the default static and template folders 
#  to fit the Vue output format.
# See Stackoverflow second answer:
# https://stackoverflow.com/questions/46214132/how-can-i-combine-vue-js-with-flask
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

""" Postgre Database """
config = dotenv_values(".env.cfg")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_FULL_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


""" Rabbit MQ Lister Threads """
app.register_blueprint(rabbit_bp)
receiver_local_status.start()



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




""" RESERVATION """
@app.route('/api/requestReservation', methods=['POST'])
def request_reservation():
    if request.method != 'POST':
        return make_response("Request not a POST method")
    body = request.get_json()
    newRes = Reservation(datetime=body["datetime"], acc=body["ownerId"], lokal=body["localId"])
    addObj(newRes)
    return make_response("Added Reservation")

@app.route('/api/statusReservation', methods=['POST'])
def status_reservation():
    if request.method != 'POST':
        return make_response("Request not a POST method")
    body = request.get_json()
    res = db.session.query(Reservation).get(body["reservationId"])
    if not res:
        return make_response("Error: Reservation doesn't exist")
    if body["accepted"]:
        res.accepted = True
        return make_response("Reservation accepted.")
    else: 
        db.session.delete(res)
        db.session.commit()
        return make_response("Reservation deleted.")




""" ACCOUNT """
@app.route('/api/createAccount', methods=['POST'])
def create_account():
    if request.method != 'POST':
        return make_response("Request not a POST method")
    body = request.get_json()
    newAcc = Account(name=body["lastname"], street=body["address"], plz=body["plz"])
    addObj(newAcc)
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