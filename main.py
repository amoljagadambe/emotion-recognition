import os
import time
from flask import Flask, jsonify, render_template, request
from classifier.emotion_classifier import EmotionClassifier
from recorder import Recorder, trim_audio_ffmpeg, filename
from remove_noise import remove_noise
from feat_util import speech_segments_with_vad

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
classifier = EmotionClassifier()
rfile = Recorder(channels=2)
filename = filename()
fname = os.path.join('recorded_audio', filename)
print("filepath :",fname)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @app.route('test', methods=['POST'])
# def audd():
#     record_to_file('test_web.wav')
#     print('ok')
"""
    with rec.open('nonblocking.wav', 'wb') as recfile2:
        recfile2.start_recording()
        time.sleep(5.0)
        recfile2.stop_recording()
"""


@app.route('/start_recording/')
def start_recording():
    # fname = filename()
    # rfile = Recorder(channels=2)
    rfile.start_recording(fname, 'wb')
    time.sleep(5.0)
    rfile.stop_recording()
    # remove noise
    nr_audio = fname[:-4] + '_nr.wav'
    if not remove_noise(fname, nr_audio, False):
        print("noise reduction not done yet!")
    else:
        sp_seg = speech_segments_with_vad(nr_audio)
        dst = fname[:-4] + '_trim.wav'
        dst_file = trim_audio_ffmpeg(nr_audio, sp_seg[0], sp_seg[1], dst)
    return render_template('index.html', message=dst_file)



@app.route('/stop_recording/<rfile>', methods=['POST'])
def stop_recording(rfile):
    rfile.stop_recording()


@app.route('/evaluateresult/')
def evaluateresult():
    file_path = filename
    if os.path.exists(file_path):
        predicted_emotion_array = classifier.classify_audio(file_path)
        print(predicted_emotion_array[0])
        print(type(predicted_emotion_array[0]))
        message = str(predicted_emotion_array[0])
    else:
        message = "FILE NOT FOUND!"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)
