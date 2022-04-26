from flask import Flask, jsonify, render_template, url_for

# To combine the build frontend with the backend 
# I changed the default static and template folders 
# to fit the Vue output format 
# see Stackoverflow second answer
# https://stackoverflow.com/questions/46214132/how-can-i-combine-vue-js-with-flask
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')

if __name__ == '__main__':
    app.run(debug=True)