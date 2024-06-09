import base64
import json
import csv
from requests import post, get

def getToken(client_id, client_secret):
    auth_string = client_id + ':' + client_secret
    auth_b64 = base64.b64encode(auth_string.encode('utf-8'))
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_b64.decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def getAuthHeader(token):
    return {'Authorization': 'Bearer ' + token}

def getAudioFeatures(token, trackId, dataset2):
    url = f'https://api.spotify.com/v1/audio-features/{trackId}'
    headers = getAuthHeader(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    audio_features_temp = [
        json_result['danceability'],
        json_result['energy'],
        json_result['key'],
        json_result['loudness'],
        json_result['mode'],
        json_result['speechiness'],
        json_result['acousticness'],
        json_result['instrumentalness'],
        json_result['liveness'],
        json_result['valence'],
        json_result['tempo'],
    ]
    dataset2.append(audio_features_temp)

def getPlaylistItems(token, playlistId):
    dataset = []
    dataset2 = []
    dataset3 = []
    url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'
    limit = '&limit=100'
    market = '?market=ID'
    fields = '&fields=items%28track%28id%2Cname%2Cartists%2Cpopularity%2C+duration_ms%2C+album%28release_date%29%29%29'
    url = url+market+fields+limit
    headers = getAuthHeader(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    for i in range(len(json_result['items'])):
        playlist_items_temp = []
        playlist_items_temp.append(json_result['items'][i]['track']['id'])
        playlist_items_temp.append(json_result['items'][i]['track']['name'].encode('utf-8'))
        playlist_items_temp.append(json_result['items'][i]['track']['artists'][0]['name'].encode('utf-8'))
        playlist_items_temp.append(json_result['items'][i]['track']['popularity'])
        playlist_items_temp.append(json_result['items'][i]['track']['duration_ms'])
        playlist_items_temp.append(int(json_result['items'][i]['track']['album']['release_date'][0:4]))
        dataset.append(playlist_items_temp)
        
    for i in range(len(dataset)):
        getAudioFeatures(token, dataset[i][0], dataset2)

    for i in range(len(dataset)):
        dataset3.append(dataset[i]+dataset2[i])
        
    with open('dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "artist", "popularity", "duration_ms", "year", "danceability", "energy", "key", "loudness", "mode",
                         "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"])
        writer.writerows(dataset3)
