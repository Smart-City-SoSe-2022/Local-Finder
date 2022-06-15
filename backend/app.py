from flask import Flask, jsonify, make_response, render_template, request_started, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from rabbit import rabbit_bp, receiver_local_status
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal, addObj
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
config = dotenv_values(".env")
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
    print(res)
    if not res:
        return make_response("Error: Reservation doesn't exist")
    if body["accepted"]:
        res.accepted = True
        db.session.commit()
        return make_response("Reservation accepted.")
    else: 
        db.session.delete(res)
        db.session.commit()
        return make_response("Reservation deleted.")

@app.route('/api/getReservations', methods=['GET'])
def get_Reservations():
    if request.method != 'GET':
        return make_response("Request not a GET method")
    body = request.get_json()
    acc = db.session.query(Account).get(body["id"])
    if not acc:
        return make_response("Account doesn't exsist.")
    reservations = []
    for r in acc.reservation:
        reservations.append(
            {
                "id": r._id,
                "datetime": r.datetime,
                "reservedLocalId": r.reservedLocal,
                "reservedLocalName": db.session.query(Lokal).get(r.reservedLocal).name
            }
        )
    return jsonify(reservations)


@app.route('/api/getLokalReservations', methods=['GET'])
def get_Lokal_Reservations():
    if request.method != 'GET':
        return make_response("Request not a GET method")
    body = request.get_json()
    lokal = db.session.query(Lokal).get(body["id"])
    if not lokal:
        return make_response("Lokal doesn't exsist.")
    reservations = []
    for r in lokal.reservation:
        reservations.append(
            {
                "id": r._id,
                "datetime": r.datetime,
                "reservedBy": r.reservedBy,
                "reservedByName": db.session.query(Account).get(r.reservedBy).name
            }
        )
    return jsonify(reservations)




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



""" Favorites """
@app.route('/api/toggleFavorite', methods=['POST'])
def toggle_favorite():
    if request.method != 'POST':
        return make_response("Request not a POST method")
    body = request.get_json()
    acc = db.session.query(Account).get(body['AccountId'])
    lokal = db.session.query(Lokal).get(body['lokalId'])
    if not acc or not lokal:
        return make_response("Account or Local doesn't exsist.")
    for f in acc.favorites:
        if f._id == lokal._id:
            acc.favorites.remove(lokal)
            db.session.commit()
            return make_response('Local has been unfavored.')
    acc.favorites.append(lokal)
    db.session.commit()
    return make_response("Local has been favored.") 


@app.route('/api/getFavorites', methods=['GET'])
def get_favorites():
    if request.method != 'GET':
        return make_response("Request not a GET method")
    body = request.get_json()
    acc = db.session.query(Account).get(body["id"])
    if not acc:
        return make_response("Account doesn't exsist.")
    print(acc.favorites)
    favorites = []
    for lokal in acc.favorites:
        favorites.append(
            {
                "id": lokal._id,
                "name": lokal.name
            }
        )
    return jsonify(favorites)



""" LOKAL """
@app.route('/api/deleteLokal', methods=['DELETE'])
def delete_lokal():
    if (request.method != 'DELETE'):
        return make_response('Request not a DELETE method')
    body = request.get_json()
    delLok = db.session.query(Lokal).get(body["id"])
    if not delLok:
        return make_response("Local doesn't exist.")
    db.session.delete(delLok)
    db.session.commit()
    return make_response("Local deletet.")

@app.route('/api/getLokals', methods=['GET'])
def get_lokals():
    if request.method != 'GET':
        return make_response("Request not a GET method")
    lokals = db.session.query(Lokal)
    returnedLokals = []
    for lokal in lokals:
        returnedLokals.append(
            {
                "id": lokal._id,
                "name": lokal.name
            }
        )
    return jsonify(returnedLokals)

if __name__ == '__main__':
    app.run(debug=True)