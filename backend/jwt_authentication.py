from flask import make_response, request
from dbModels import Account, db
from dotenv import dotenv_values
import jwt
from functools import wraps

config = dotenv_values(".env")

""" JWT Wrapper """
def token_requierd(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'JWT' in request.cookies:
            token = request.cookies['JWT']
        if not token:
            return make_response('Token fehlt!'), 401
        try:
            data = jwt.decode(token, config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = db.session.query(Account).get(data['sub'])
            if not current_user :
                return make_response('Token ist ungültig'), 401
        except Exception as e:
            return make_response('Token ist ungültig!'), 401
        return f(current_user, *args, **kwargs)
    return decorated