import requests
import webbrowser
from config import SOUNDCLOUD_CLIENT_ID, SOUNDCLOUD_CLIENT_SECRET, SOUNDCLOUD_REDIRECT_URI

class SoundCloudAuth:
    def __init__(self):
        self.client_id = SOUNDCLOUD_CLIENT_ID
        self.client_secret = SOUNDCLOUD_CLIENT_SECRET
        self.redirect_uri = SOUNDCLOUD_REDIRECT_URI

    def get_auth_url(self):
        # URL de autorización de SoundCloud
        auth_url = f'https://soundcloud.com/connect?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope=non-expiring+upload'
        webbrowser.open(auth_url)
        print("Se ha abierto la URL para autorizar la aplicación en el navegador.")

    def get_access_token(self, authorization_code):
        # Intercambiar el código de autorización por un token de acceso
        token_url = 'https://api.soundcloud.com/oauth2/token'
        token_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            raise Exception(f"Error al obtener el token de acceso de SoundCloud: {response.status_code}")

class SoundCloudAPI:
    def __init__(self, access_token):
        self.access_token = access_token

    def add_to_favorites(self, track_id):
        url = f'https://api.soundcloud.com/me/favorites'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        data = {
            'track_id': track_id
        }
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 201:
            print("Canción agregada a favoritos.")
        else:
            print(f"Error al agregar canción a favoritos: {response.status_code}")
