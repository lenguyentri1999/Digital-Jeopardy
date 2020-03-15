from flask import Flask, jsonify, render_template, send_file, request
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, db
import json

#app = Flask(__name__, static_folder='public', static_url_path='')
app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("db_private_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://cs-530-digital-jeopardy.firebaseio.com"
})


@app.route('/games', methods=['GET'])
def getGames():
    ref = db.reference('games')
    return jsonify(ref.get())

@app.route('/create-game', methods=['POST'])
def createGame():
    print("creating game...")
    game = request.json['game']
    game = json.loads(game)
    print(game)
    ref = db.reference('games/' + game['id'])
    ref.update(game)
    return jsonify(gamekey=game['id'])


@app.route('/send-score', methods=['POST'])
def sendScore():
    print("adding score...")
    name = request.json['name']
    score = request.json['score']
    id = request.json['id']
    print(id)
    ref = db.reference('scores/' + id)
    ref.push({"name": name, "score": score})
    return jsonify(done='true')
    

@app.route('/get-score', methods=['POST'])
def getScore():
    print("getting score...")
    id = request.json['id']
    print(id)
    ref = db.reference('scores/' + id)
    return jsonify(ref.get())

# # Handle the index (home) page
# @app.route('/')
# def index():
#     return render_template('index.html')


# # Handle the index (home) page
# @app.route('/bikes')
# def bikes():
#     return render_template('bikes.html', bikeLength=len(bikeData), bikeData = bikeData)


# # Handle any files that begin "/course" by loading from the course directory
# @app.route('/course/<path:path>')
# def base_static(path):
#     return send_file(os.path.join(app.root_path, '..', 'course', path))

# # Handle any files that begin "/a1" by loading from the a1 directory
# @app.route('/a1/<path:path>')
# def a1_static(path):
#     return send_file(os.path.join(app.root_path, '..', 'a1', path))


# # Handle any unhandled filename by loading its template
# @app.route('/<name>')
# def generic(name):
#     return render_template(name + '.html')


# Any additional handlers that go beyond simply loading a template
# (e.g., a handler that needs to pass data to a template) can be added here


if __name__ == "__main__":

    production = True
    myPort = 8126
    if production:
        app.run(host='0.0.0.0', port=myPort)
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)
