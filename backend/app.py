from flask import Flask, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

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

db = SQLAlchemy(app)
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
    task = Test(content="Hallo ich bin ein Beispiel. HALLO")
    try: 
        db.session.add(task)
        db.session.commit()
        return jsonify('pong')
    except:
        return 'Faield to commit to the Database. app.route/ping'

if __name__ == '__main__':
    app.run(debug=True)