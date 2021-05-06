from flask import Flask, render_template, Response, jsonify
from camera import VideoCamera
import os

pred = "Neutral"
songs_list = dict()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global pred
    while True:
        frame = camera.get_frame()
        pred = frame[1]
        frame = frame[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/_get_songs')
def get_songs():
    global songs_list
    if pred in songs_list:
        songs = songs_list[pred]
    return jsonify(songs)

if __name__ == '__main__':
    directory = "./static/music"
    for foldername in os.listdir(directory):
        songs_list[foldername] = []
        for songs in os.listdir(directory + "/" + foldername):
            songs_list[foldername].append({"name":songs.split(".mp3")[0], "path":"/static/music/"+foldername+"/"+songs, "img":"", "singer":""})

    app.run(host='0.0.0.0', debug=True)
