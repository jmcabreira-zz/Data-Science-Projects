import os.path
from flask import Flask, render_template,request
import os
import json
import time
from datetime import datetime
import pandas as pd
from ml_utils import *
import pickle
import joblib as jb

import spotipy
import spotipy.util as util 
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '7caa94d5897b435abdd6fc9e06bb8f04'
client_secret = '694e12a56652423194e4f092e7304f2b'
redirect_uri = 'http://localhost:8000/' 
user_id = '12162753154'

token = util.prompt_for_user_token(user_id,
                                  'playlist-read-collaborative',
                                  client_id = client_id,
                                  client_secret = client_secret,
                                  redirect_uri = redirect_uri)

sp = spotipy.Spotify(auth = token)

app = Flask(__name__)
scaler = pickle.load(open("models/MinMaxScaler.pickle", "rb"))
lr_model = jb.load('models/lr_modeel.pk.z')
model_lgbm = jb.load('models/lgbm_model.pk;.z')

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
    #port = int(os.environ.get('PORT', 8000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug = True)


