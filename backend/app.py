from hashlib import algorithms_available
from flask import Flask, jsonify, make_response, render_template, request_started, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from rabbit import rabbit_bp, receiver_local_status, receiver_acc_created, receiver_acc_deleted
from flask_migrate import Migrate
from dbModels import db, Account, Reservation, Lokal, LokalType, addObj
from dotenv import dotenv_values
from flask_cors import CORS
import jwt
from jwt_authentication import token_requierd

app = Flask(__name__)
CORS(app, supports_credentials=True)

""" Postgre Database """
config = dotenv_values(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_FULL_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


""" Rabbit MQ Lister Threads """
app.register_blueprint(rabbit_bp)
receiver_local_status.start()
receiver_acc_created.start()
receiver_acc_deleted.start()



"""""""""""""""""""""""
    Routing Paths 
"""""""""""""""""""""""

@app.route('/api/search', methods=['POST'])
def search():
    body = request.get_json()
    name = body['name']
    typ = body['type']
    city = body['city']
    objectList = []
    if name != "":
        objectList = db.session.query(Lokal).filter(Lokal.name.like('%'+name+'%')).all()
        if not objectList:
            return make_response('Lokal \"'+name+'\" wurde nicht gefunden.'), 400
    if typ != "":
        lokalTyp = db.session.query(LokalType).filter(LokalType._type.like(typ)).first()
        if not lokalTyp: 
            return make_response('Lokal Typ \"'+typ+'\" wurde nicht gefunden.'), 400
        if objectList != []:
            newList =  []
            for lok in lokalTyp.lokals:
                for obj in objectList:
                    if obj._id == lok._id:
                        newList.append(obj)
                        break
            objectList = newList
            if objectList == []:
                return  make_response('Lokal Typ \"'+typ+'\" wurde nicht gefunden.'), 400
        else:
            for obj in lokalTyp.lokals:
                objectList.append(obj)
    if city != "":
        cityList = db.session.query(Lokal).filter(Lokal.city.like('%'+city+'%')).all()
        if not cityList:
            return make_response('Zur Stadt \"'+city+'\" wurde nichts gefunden.'), 400
        if objectList != []:
            newList = []
            for obj in cityList:
                if objectList.__contains__(obj):
                    newList.append(obj)
            objectList = newList
        else:
            objectList = cityList
    retList = []
    for lokal in objectList:
        retList.append(
            {
                "id": lokal._id,
                "name": lokal.name,
                "address": f"{lokal.address}, {lokal.plz} {lokal.city}",
                "types": [result.serialized for result in lokal.types]
            }
        )
    return jsonify(retList)


""" RESERVATION """
@app.route('/api/requestReservation', methods=['POST'])
@token_requierd
def request_reservation(acc):
    body = request.get_json()
    newRes = Reservation(datetime=body["datetime"], acc=acc._id, lokal=body["localId"])
    addObj(newRes)
    return make_response("Added Reservation")

@app.route('/api/statusReservation', methods=['POST'])
@token_requierd
def status_reservation(acc):
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
@token_requierd
def get_Reservations(acc):
    reservations = []
    for r in acc.reservation:
        lok = db.session.query(Lokal).get(r.reservedLocal)
        reservations.append(
            {
                "id": r._id,
                "datetime": r.datetime,
                "address": f"{lok.address}, {lok.plz} {lok.city}",
                "types": [result.serialized for result in lok.types],
                "reservedLocalId": r.reservedLocal,
                "reservedName": lok.name
            }
        )
    return jsonify(reservations)

@app.route('/api/getLokalReservations', methods=['GET'])
@token_requierd
def get_Lokal_Reservations(acc):
    lokal = db.session.query(Lokal).get(request.args.get("id"))
    if not lokal:
        return make_response("Lokal doesn't exsist."), 501
    reservations = []
    for r in lokal.reservation:
        reservations.append(
            {
                "id": r._id,
                "datetime": r.datetime,
                "reservedBy": r.reservedBy,
                "reservedName": db.session.query(Account).get(r.reservedBy).name
            }
        )
    return jsonify(reservations)



""" Favorites """
@app.route('/api/toggleFavorite', methods=['POST'])
@token_requierd
def toggle_favorite(acc):
    body = request.get_json()
    lokal = db.session.query(Lokal).get(body['lokalId'])
    if not lokal:
        return make_response("Local doesn't exsist.")
    for f in acc.favorites:
        if f._id == lokal._id:
            acc.favorites.remove(lokal)
            db.session.commit()
            return make_response('Local has been unfavored.')
    acc.favorites.append(lokal)
    db.session.commit()
    return make_response("Local has been favored.") 

@app.route('/api/getFavorites', methods=['GET'])
@token_requierd
def get_favorites(acc):
    if not acc:
        return make_response("Account doesn't exsist.")
    favorites = []
    for lokal in acc.favorites:
        favorites.append(
            {
                "id": lokal._id,
                "name": lokal.name,
                "types": [result.serialized for result in lokal.types],
            }
        )
    return jsonify(favorites)

@app.route('/api/isFavorite', methods=['POST'])
@token_requierd
def is_favorite(acc):
    body = request.get_json()
    lok = db.session.query(Lokal).get(body["lokId"])
    if lok in acc.favorites:
        return make_response("True")
    return make_response("False"), 501



""" LOKAL """
@app.route('/api/deleteLokal', methods=['DELETE'])
@token_requierd
def delete_lokal(acc):
    body = request.get_json()
    delLok = db.session.query(Lokal).get(body["id"])
    if not delLok:
        return make_response("Local doesn't exist.")
    db.session.delete(delLok)
    db.session.commit()
    return make_response("Local deletet.")

@app.route('/api/getLokals', methods=['GET'])
def get_lokals():
    lokals = db.session.query(Lokal)
    returnedLokals = []
    for lokal in lokals:
        returnedLokals.append(
            {
                "id": lokal._id,
                "name": lokal.name,
                "types": [result.serialized for result in lokal.types],
                "address": f"{lokal.address}, {lokal.plz} {lokal.city}",
            }
        )
    return jsonify(returnedLokals)

@app.route('/api/getLokal', methods=['GET'])
def get_lokal():
    lok = db.session.query(Lokal).get(request.args.get("id"))
    return jsonify({ 
        "name": lok.name,
        "address": lok.address,
        "plz": lok.plz,
        "city": lok.city
    })

@app.route('/api/isOwner', methods=['GET'])
@token_requierd
def is_owner(acc):
    lokale = db.session.query(Lokal)
    for lok in lokale:
        if lok.owner == acc._id:
            return make_response("True") 
    return make_response("False")

@app.route('/api/getOwningLokals', methods=['GET'])
@token_requierd
def get_owning_lokals(acc):
    lokals = db.session.query(Lokal)
    returnedLokals = []
    for lokal in lokals:
        if lokal.owner == acc._id: 
            returnedLokals.append(
                {
                    "id": lokal._id,
                    "name": lokal.name,
                    "types": [result.serialized for result in lokal.types],
                    "address": f"{lokal.address}, {lokal.plz} {lokal.city}",
                }
        )
    return jsonify(returnedLokals)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)