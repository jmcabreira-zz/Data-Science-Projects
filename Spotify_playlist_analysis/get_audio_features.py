
def get_audio_features(playlist_id, playlist_name, sp , data_dir = 'audio_features'):  
    
    """Gets audio features of each song of each individual playlist and save it in a json file
    
    PARAMETERS: 
    playlist_id(list): A list containing id of each playlist
    playlist_name(list): A list with names of each playlist
    sp(spotipy object) : An object that provides access to the Spotify API
    
    RETURNS:
    A json file with audio features of each song
    """
    
    features_data = {}
    
    for playlist_id, playlist_name in zip( playlists_id_list, playlist_name_list) :

        #tracks of each playlist
        tracks = sp.playlist_tracks(playlist_id)

        for track in tracks['items']:

            song_name  = track['track']['name']
            song_id = track['track']['id']

            #print(song_name)
            features = sp.audio_features(song_id)

            # make data dir, if it does not exist
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            with open("./audio_features/audio_features.json", "a+") as output:


                features_data['playlist_name'] = playlist_name
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
                features_data['id'] = features[0]['id']

                output.write("{}\n".format(json.dumps(features_data)))

        print("playlist name: {}, has been added ".format(playlist_name))
