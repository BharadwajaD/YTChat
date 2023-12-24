from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

from dataStore import DataStore

app = Flask(__name__)
CORS(app)

ds = DataStore()

@app.route('/', methods=['POST'])
def start():

    uid = ds.insert_user()
    video_id = request.get_data().decode('utf-8')

    formatter = JSONFormatter()
    transcript = formatter.format_transcript(YouTubeTranscriptApi.get_transcript(video_id))

    ds.insert_message(uid, 'Transcript:', transcript)

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
