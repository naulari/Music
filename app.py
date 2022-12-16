from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests, spotipy
import config
app=Flask(__name__, template_folder='template')

cid = config.client_id
secret = config.client_secret
uri= config.redirect_uri
oathmanager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri)
sp = spotipy.Spotify(oauth_manager=oathmanager) 


@app.route('/',methods =["POST", "GET"])
def get_songs():
    if request.method == "POST":
        
        artist = "\""+ request.form.get("artist") + "\""

        url = "https://genius.p.rapidapi.com/search"

        querystring = {"q": artist}

        headers = {
            'x-rapidapi-host': "genius.p.rapidapi.com",
            'x-rapidapi-key': config.api_key
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        obj = response.json()

        artistDict = {}
        for i in range(10):
            if obj["response"]['hits'][i]["result"]["primary_artist"]["name"] not in artistDict:
                artistDict[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] = 1
            else:
                artistDict[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] += 1

        artist = max(artistDict, key=artistDict.get)
    
        infoDict = {'songs':[], 'artists':[],'imgs':[]}

        for i in range(3):
            infoDict['songs'].append(obj['response']['hits'][i]['result']['title'])
            infoDict['artists'].append(obj['response']['hits'][i]['result']['artist_names'])
            infoDict['imgs'].append(obj['response']['hits'][i]['result']["song_art_image_url"])

        URLs = spotipyPreview(infoDict, artist)

        return render_template("index.html", artist_name=artist, song1 = infoDict['songs'][0], \
            song2=infoDict['songs'][1], song3=infoDict['songs'][2], song1img=infoDict['imgs'][0], \
            song2img=infoDict['imgs'][1], song3img=infoDict['imgs'][2], song1artists=infoDict['artists'][0],\
            song2artists=infoDict['artists'][1], song3artists=infoDict['artists'][2], song1url=URLs[0], \
            song2url=URLs[1], song3url=URLs[2])
    else:
        return render_template("index.html")


def spotipyPreview(dict, artist):
    URLs = []
    for s in dict['songs']:
        result = sp.search(q=f'track:{s} artist:{artist}',type='track', limit=1)
        URLs.append(result['tracks']['items'][0]['preview_url'])

    return URLs

if __name__ == '__main__':
    app.run(debug=True,port="8990")