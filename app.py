from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import requests, json, sys, spotipy
import config
app=Flask(__name__, template_folder='template')

@app.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        get_songs()
    else:
        return render_template('home.html')


@app.route('/results',methods =["POST", "GET"])
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

        '''
        counter = 0
        while obj['response']['hits'][counter]['result']['primary_artist']['is_verified'] == False:
            counter += 1
            if counter >= len(obj['response']['hits']):
                counter=0
                break
        artist=obj['response']['hits'][counter]['result']['primary_artist']['name']
        '''

        artistDict = {}
        for i in range(10):
            if obj["response"]['hits'][i]["result"]["primary_artist"]["name"] not in artistDict:
                artistDict[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] = 1
            else:
                artistDict[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] += 1

        artist=max(artistDict, key=artistDict.get)
    
        infoDict = {'songs':[], 'artists':[],'imgs':[]}

        for i in range(3):
            infoDict['songs'].append(obj['response']['hits'][i]['result']['title'])
            infoDict['artists'].append(obj['response']['hits'][i]['result']['artist_names'])
            infoDict['imgs'].append(obj['response']['hits'][i]['result']["song_art_image_url"])
        

        IDs = spotipyIDs(infoDict,artist)

        URLs = spotipyPreview(IDs)

        return render_template("index.html", artist_name=artist, song1 = infoDict['songs'][0], \
            song2=infoDict['songs'][1], song3=infoDict['songs'][2], song1img=infoDict['imgs'][0], \
            song2img=infoDict['imgs'][1], song3img=infoDict['imgs'][2], song1artists=infoDict['artists'][0],\
            song2artists=infoDict['artists'][1], song3artists=infoDict['artists'][2], song1url=URLs[0], \
            song2url=URLs[1], song3url=URLs[2])
    else:
        return render_template("index.html")

def spotipyIDs(dict,artist):
    '''
    cid = config.client_id
    secret = config.client_secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
    #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    '''
    cid = config.client_id
    secret = config.client_secret
    uri= config.redirect_uri
    oathmanager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri)
    sp = spotipy.Spotify(oauth_manager=oathmanager) 

    for i in artist:
        if i == ' ':
            artist = artist.replace(' ','')
    
    results = []
    for i in range(3):
        results.append(sp.search(q='track:'+dict['songs'][i], type='track', limit=1))
    print(results)
    '''
    for i in range(3):
        print(results[i]['tracks']['items'][0]['name'])
        print(results[i]['tracks']['items'][0]['album']['images'][0]['url'])
        print(results[i]['tracks']['items'][0]['id'])
        print(results[i]['tracks']['items'][0]['preview_url'])
        print()
    print()
    '''
    IDs = []
    for i in range(3):
        IDs.append(results[i]['tracks']['items'][0]['id'])

    return IDs

def spotipyPreview(IDs):
    '''
    cid = config.client_id
    secret = config.client_secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
    #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    '''
    cid = config.client_id
    secret = config.client_secret
    uri= config.redirect_uri
    oathmanager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=uri)
    sp = spotipy.Spotify(oauth_manager=oathmanager) 

    URLs = []
    for i in range(3):
        #print(sp.track(IDs[i]))
        URLs.append(sp.track(IDs[i])['preview_url'])

    return URLs


def spotifyIDs(dict,artist):
    url = "https://spotify23.p.rapidapi.com/search/"

    headers = {
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
        "X-RapidAPI-Key": config.api_key
    }
    
    results = []

    for i in range(3):
        querystring = {"q":dict['songs'][i] + " " + artist,"type":"tracks","offset":"0","limit":"1","numberOfTopResults":"5"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        results.append(response.json())
    
    #for i in range(3):
    #    print(results[i]['tracks']['items'][0]['data']['name'], file=sys.stdout)
    #    print(results[i]['tracks']['items'][0]['data']['id'], file=sys.stdout)
    #    print()

    IDs = []
    for i in range(3):
        IDs.append(results[i]['tracks']['items'][0]['data']['id'])

    return IDs

def spotifyPreview(IDs):
    url = "https://spotify23.p.rapidapi.com/tracks/"

    headers = {
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
        "X-RapidAPI-Key": config.api_key
    }
    
    results = []

    for i in range(3):
        querystring = {"ids":IDs[i]}
        response = requests.request("GET", url, headers=headers, params=querystring)
        results.append(response.json())

    #for i in range(3):
    #    print(results[i]['tracks'][0]['preview_url'], file=sys.stdout)
    #    print()
    
    urls = []
    for i in range(3):
        urls.append(results[i]['tracks'][0]['preview_url'])

    return urls

if __name__ == '__main__':
    app.run(debug=True,port="8990")