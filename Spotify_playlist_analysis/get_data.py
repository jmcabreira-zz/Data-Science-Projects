def get_playlists_information(user_id, sp, data_dir = 'playlists_info'):
	'''Pull playlist list information for a given user id

	PARAMETERS:
	user_id(string): The user id
	sp(spotipy object) : An object that provides access to the Spotify API
	data_dir(string): The name of the foldec in which the data will be stored

	RETURNS:
	Playlist information as a json file '''
    
    playlists = sp.user_playlists(user_id)
    
    for playlist in playlists['items']:
        
        playlist_name = playlist['name']
        number_of_songs = playlist['tracks']['total']
        playlist_id = playlist['id']
        
        
        if not playlist_name.strip():
            pass
        
        else:
        
        
            # make data dir, if it does not exist
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            with open("./playlists_info/playlists.json", "a+") as output:

                data = {'playlist_name': playlist_name,
                       "number_of_songs": number_of_songs,
                       "playlist_id": playlist_id}

                output.write("{}\n".format(json.dumps(data)))

            print("playlist name: {}, Number of songs: {}, Playlist ID: {} ".format(playlist_name,
            number_of_songs,playlist_id))
        