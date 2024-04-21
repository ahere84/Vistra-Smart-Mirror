import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    client_id = 'cd1d79cc28bf4391959ccb50dbfc5a07'
    client_secret = 'a9e4287d0dcd48609b0d1730b3d08db1'
    redirect_uri = 'ws://127.0.0.1:43333' 
    scope = 'user-modify-playback-state user-read-playback-state'  

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope))
    return sp