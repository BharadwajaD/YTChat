from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from dataStore import DataStore

app = Flask(__name__)
CORS(app)

ds = DataStore()

@app.route('/', methods=['POST'])
def start():
    # Fetch transcript from YouTube (not implemented yet)
    uid = ds.insert_user()
    ytube_url = request.get_data().decode('utf-8')
    return jsonify(uid)

@app.route('/question', methods=['POST'])
def question():

    ques = request.get_data().decode('utf-8')
    uid = request.headers['User']
    ans = 'Generated answer ....'

    ds.insert_message(uid, ques, ans)
    print(ds)

    return jsonify(ans)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
