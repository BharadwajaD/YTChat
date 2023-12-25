from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

from dataStore import DataStore
from GenAns import QAModel

app = Flask(__name__)
CORS(app)

ds = DataStore()
qa_model = QAModel()

@app.route('/', methods=['POST'])
def start():

    uid = ds.insert_user()
    video_id = request.get_data().decode('utf-8')

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ""
    for tr in transcript_list:
        transcript += tr['text'] + ' '

    ds.insert_message(uid, 'Transcript:', transcript)
    return jsonify(uid)

@app.route('/question', methods=['POST'])
def question():

    ques = request.get_data().decode('utf-8')
    uid = request.headers['User']
    ans = qa_model.answer(ds.get_chat(uid).__str__(), ques)

    ds.insert_message(uid, ques, ans)
    return jsonify(ans)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
