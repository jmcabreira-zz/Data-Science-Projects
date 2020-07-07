import pickle
import pandas as pd
import joblib as jb


def get_one_track_features(artist, song,sp):
    
    features_data = {}
    
    search_query = sp.search(artist)
    
    for i in range(len(search_query['tracks']['items'])):
    
        if  song.lower() in search_query['tracks']['items'][i]['name'].lower(): 
            print("Música Encontrada: {} - artista(s): {}".format(search_query['tracks']['items'][i]['name'].lower(),artist))
            found_track = search_query['tracks']['items'][i]['name']  
            track_id = search_query['tracks']['items'][i]['id']
            
            features = sp.audio_features(track_id)
            
            features_data['danceability'] = features[0]['danceability']
            features_data['energy'] = features[0]['energy']
            features_data['loudness'] = features[0]['loudness']
            features_data['mode'] = features[0]['mode']
            features_data['speechiness'] = features[0]['speechiness']
            features_data['acousticness'] = features[0]['acousticness']
            features_data['instrumentalness'] = features[0]['instrumentalness']
            features_data['liveness'] = features[0]['liveness']
            features_data['valence'] = features[0]['valence']
            features_data['tempo'] = features[0]['tempo']
            
            break
        
    return features_data       


def make_prediction(data): 

    scaler = pickle.load(open("models/MinMaxScaler.pickle", "rb"))
    lr_model = jb.load('models/lr_modeel.pk.z')
    model_lgbm = jb.load('models/lgbm_model.pk;.z')

    df = pd.DataFrame([data])
    
    scaled_array = scaler.transform(df)

    if scaled_array is None:
        return 'Feature is None' 
    
    pred_lr= lr_model.predict(scaled_array)
    pred_lgbm = model_lgbm.predict(scaled_array)
    #print(pred_lr)
    #print(pred_lgbm)

    pred =  0.1*pred_lr + 0.9*pred_lgbm
 
    for i, element in enumerate(pred): 
        if element <= 0.5:
            pred[i] = 0.0
        else:
            pred[i] = 1.0 
    result = ['Essa música é recomendada para Jonathan' if pred[0] == 1 else 'Essa música é recomendada para Emily']
    
    return pred[0]