import requests
import json
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer API_KEY',
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
    
    

