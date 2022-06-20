from flask import Flask, jsonify, make_response, render_template, request_started, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
# from rabbit import rabbit_bp, receiver_local_status
from flask_migrate import Migrate
from datetime import datetime
from dbModels import db, Account, Reservation, Lokal, LokalType, addObj
from dotenv import dotenv_values
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

""" Postgre Database """
config = dotenv_values(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_FULL_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


""" Rabbit MQ Lister Threads """
# app.register_blueprint(rabbit_bp)
# receiver_local_status.start()



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
            return make_response('Lokal Typ '+typ+' wurde nicht gefunden.')
        # if typ != "":
        #     for obj in objectList:
        #         removeObj = True
        #         for _type in obj.types:
        #             if typ.lower() == _type.lower():
        #                 removeObj = False
        #         if removeObj:
        #             objectList.remove(obj)
        # if city != "":
        #     for obj in objectList:
        #         if obj.city != city:
        #             objectList.remove(obj) 
    if typ != "":
        pass
        lokalTyp = db.session.query(LokalType).filter(LokalType._type.like(typ)).first()
        if not lokalTyp: 
            return make_response('Lokal Typ '+typ+' wurde nicht gefunden.')
        if objectList != []:
            for obj in lokalTyp.lokals:
                if not objectList.__contains__(obj):
                    objectList.remove(obj)
                    print("Removed: "+obj)
        else:
            for obj in lokalTyp.lokals:
                objectList.append(obj)
    if city != "":
        cityList = db.session.query(Lokal).filter(Lokal.city.like('%'+city+'%')).all()
        if not cityList:
            return make_response('Zur Stadt '+city+' wurde nichts gefunden.')
        if objectList != []:
            newList = []
            for obj in cityList:
                print(f"checking: {obj}")
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
                "name": lokal.name
            }
        )
    return jsonify(retList)


""" RESERVATION """
@app.route('/api/requestReservation', methods=['POST'])
def request_reservation():
    body = request.get_json()
    newRes = Reservation(datetime=body["datetime"], acc=body["ownerId"], lokal=body["localId"])
    addObj(newRes)
    return make_response("Added Reservation")

@app.route('/api/statusReservation', methods=['POST'])
def status_reservation():
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
    acc = db.session.query(Account).get(request.args.get("id"))
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
    body = request.get_json()
    newAcc = Account(name=body["lastname"], street=body["address"], plz=body["plz"])
    addObj(newAcc)
    return make_response("Account Created")

@app.route('/api/deleteAccount', methods=['DELETE'])
def delete_account():
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
    acc = db.session.query(Account).get(request.args.get("id"))
    if not acc:
        return make_response("Account doesn't exsist.")
    favorites = []
    for lokal in acc.favorites:
        favorites.append(
            {
                "id": lokal._id,
                "name": lokal.name
            }
        )
    return jsonify(favorites)

@app.route('/api/isFavorite', methods=['POST'])
def is_favorite():
    body = request.get_json()
    acc = db.session.query(Account).get(body["accId"])
    lok = db.session.query(Lokal).get(body["lokId"])
    if lok in acc.favorites:
        return make_response("True")
    return make_response("False"), 501



""" LOKAL """
@app.route('/api/deleteLokal', methods=['DELETE'])
def delete_lokal():
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
                "name": lokal.name
            }
        )
    return jsonify(returnedLokals)

@app.route('/api/getLokal', methods=['GET'])
def get_lokal():
    lok = db.session.query(Lokal).get(request.args.get("id"))
    return jsonify({ "name": lok.name})



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)