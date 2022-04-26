from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Im Root'

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')

if __name__ == '__main__':
    app.run(debug=True)