import requests
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQDOYx_E-x_O2aCJuqjod0-AI8HtTtvmwoLntYyhM16qavtRMvB3fE8uVVENezN1r7kkONeBbDBx0i06lTLoAkgNruxNYEypAUdzSNvULTlCJbIeR9nneIJN5MdwB-HchaZ6tgCWigUBMnVqstSN3mQLUEGAxnkGo8VstY6i69MhxQ7wEqM8tqCtqiW_KnErrlnwAY5hT3NevAI-PPBDINQ5k86rw-FxnfA3bM5x8iG-anhfSr9SxaNxB-xonzrULhRSnbnShsql9loZVQ',
}


def play():
    response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers)

def pause():
    response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)

def getCurrentArtist():
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    current_song_dict = json.loads(response.text)
    return current_song_dict['item']['album']['artists'][0]['name']

def getCurrentAlbum():
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    current_song_dict = json.loads(response.text)
    return current_song_dict['item']['album']['name']
    
def getCurrentSong():
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    current_song_dict = json.loads(response.text)
    return current_song_dict['item']['name']

def changeVolume(volume, device_id):
    params = (
        ('volume_percent', volume),
        ('device_id', device_id),
    )
    response = requests.put('https://api.spotify.com/v1/me/player/volume', headers=headers, params=params)
    
    

