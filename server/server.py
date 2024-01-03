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

    video_id = request.get_data().decode('utf-8')

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ""

    #TODO: process the text more
    for tr in transcript_list:
        transcript += tr['text']

    context = """
    You are a chatbot for a video and you need to answer to the upcoming question 
    based on the transcript of the video...
    Transcript: {}
    """.format(transcript)

    uid = ds.insert_user(context)
    return jsonify(uid)

@app.route('/question', methods=['POST'])
def question():

    ques = request.get_data().decode('utf-8')
    uid = request.headers['User']
    ans = ds.insert_message(uid, ques)

    return jsonify(ans)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
