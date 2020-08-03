import pickle
import joblib as jb

model_rf = jb.load('models/rf_model.pk.z')
model_lgbm = jb.load('models/lgbm_model.pk.z')


def get_one_track_features(artist, song,sp):
    
    """ Acessa a API do spotify e acessa os audio features de uma decterminada música
    ARG: 
    artist(string): String informando nome do artista a ser pesquisado
    song:(string): String informando nome da música a ser pesquisada
    sp(spotipy object): Chace ve acesso a API 
    RETURNS:
    features_data(dictionary): Dicionário contendo as audio features"""
    
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
            
            #loudness = Normalize_value(features[0]['loudness'], loudness = True )
            #loudness = round(loudness,4)
            #features_data['loudness'] = loudness
            features_data['loudness'] = round(Normalize_value(features[0]['loudness'], loudness = True ),2)
            
            
            features_data['mode'] = features[0]['mode']
            features_data['speechiness'] = features[0]['speechiness']
            features_data['acousticness'] = features[0]['acousticness']
            features_data['instrumentalness'] = features[0]['instrumentalness']
            features_data['liveness'] = features[0]['liveness']
            features_data['valence'] = features[0]['valence']
            
            #tempo = Normalize_value( features[0]['tempo'] )
            #tempo = round(tempo,4)
            #features_data['tempo'] = tempo
            features_data['tempo'] = round(Normalize_value( features[0]['tempo'] ),4)
                  
            break
            
    return features_data       

def make_prediction(data):
    
    """ Realiza a predição com base na combinação dois algoritmos de machine learning (Ensemble model)
    ARG:
    data(dictionary): Dicionário contendo as audio features

    RETURNS: 
    classe (float): Float que representa a classe predita"""

    
    data = ([list(data.values())])
    #print(data)

    pred_rf= model_rf.predict(data)
    pred_lgbm = model_lgbm.predict(data)
    
    #print(pred_rf)
    #print(pred_lgbm)

    pred =  0.4*pred_rf + 0.6*pred_lgbm
  
    for i, element in enumerate(pred): 
        if element < 1:
            pred[i] = 0.0
        else:
            pred[i] = 1.0
    
    #result = ['Música para o Jhon' if pred[0] == 1 else 'Música para a Emy']
    
    
    return pred[0]

def Normalize_value(feature, loudness = False): 
    ''' Normaliza tempo e loudness e pega valor absoluto caso parâmetro passado seja loudness

    ARG: 

    tempo(float): Feature que será normalizada
    loudness(float): Feature que será normalizada e calculado valor absoluto
 
    RETURNS: 
    --
    '''
    Max_tempo = 204.225
    Max_loudness = 44.761
    Min_tempo = 52.24
    Min_loudness = 0.04
    
    if loudness:
        feature = (feature - Min_loudness) / (Max_loudness - Min_loudness)     
        return  abs(feature)
    
    else:        
        feature = (feature - Min_tempo) / (Max_tempo - Min_tempo)
    
        return feature
    