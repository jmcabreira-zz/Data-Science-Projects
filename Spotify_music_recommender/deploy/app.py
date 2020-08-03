from flask import Flask, render_template,request
from ml_utils import *


import spotipy
import spotipy.util as util 
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'your_client_id'
client_secret = 'yout_client_secret'
redirect_uri = 'http://localhost:8080/' 
#redirect_uri = 'https://spt-recommender.herokuapp.com/' 
user_id = 'your_user_id'

token = util.prompt_for_user_token(user_id,
                                  'playlist-read-collaborative',
                                  client_id = client_id,
                                  client_secret = client_secret,
                                  redirect_uri = redirect_uri)

sp = spotipy.Spotify(auth = token)

# create an instance of Flask class
app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        song = request.form['music']
        artist = request.form['artist']

        features_data = get_one_track_features(artist, song,sp)
        pred = make_prediction(features_data)   
        return render_template("result.html",result = result, pred = pred)

if __name__ == "__main__":
    app.run(debug = True)


