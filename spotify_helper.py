import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

# Scopes necesarios para leer tus playlists
SCOPE = "playlist-read-private playlist-read-collaborative user-top-read"

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    ))
    return sp

def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        tracks.append({
            'name': track_name,
            'artist': artists
        })
    return tracks
