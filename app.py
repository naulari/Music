from flask import Flask, render_template, request
import requests, json
import config
from pytube import Search
app=Flask(__name__, template_folder='template')

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

        '''
        counter = 0
        while obj['response']['hits'][counter]['result']['primary_artist']['is_verified'] == False:
            counter += 1
            if counter >= len(obj['response']['hits']):
                counter=0
                break
        artist=obj['response']['hits'][counter]['result']['primary_artist']['name']
        '''

        artistDic = {}
        for i in range(10):
            if obj["response"]['hits'][i]["result"]["primary_artist"]["name"] not in artistDic:
                artistDic[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] = 1
            else:
                artistDic[obj["response"]['hits'][i]["result"]["primary_artist"]["name"]] += 1

        artist=max(artistDic, key=artistDic.get)
    
        infoDic = {'songs':[], 'artists':[],'imgs':[]}

        for i in range(3):
            infoDic['songs'].append(obj['response']['hits'][i]['result']['title'])
            infoDic['artists'].append(obj['response']['hits'][i]['result']['artist_names'])
            infoDic['imgs'].append(obj['response']['hits'][i]['result']["song_art_image_url"])

        return render_template("index.html", artist_name=artist, song1 = infoDic['songs'][0], \
            song2=infoDic['songs'][1], song3=infoDic['songs'][2], song1img=infoDic['imgs'][0], \
            song2img=infoDic['imgs'][1], song3img=infoDic['imgs'][2], song1artists=infoDic['artists'][0],\
            song2artists=infoDic['artists'][1], song3artists=infoDic['artists'][2],)
    else:
        return render_template("index.html")





if __name__ == '__main__':
    app.run(debug=True,port="8990")