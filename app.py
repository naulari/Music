from flask import Flask, render_template, request
import requests, json
import config
app=Flask(__name__, template_folder='template')

@app.route('/',methods =["POST", "GET"])
def get_songs():
    if request.method == "POST":
        
        artist = request.form.get("artist")

        url = "https://genius.p.rapidapi.com/search"

        querystring = {"q": artist}

        headers = {
            'x-rapidapi-host': "genius.p.rapidapi.com",
            'x-rapidapi-key': config.api_key
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        obj = response.json()
        song1 = obj["response"]["hits"][0]["result"]["title"]
        song2 = obj["response"]["hits"][1]["result"]["title"]
        song3 = obj["response"]["hits"][2]["result"]["title"]

        song1img = obj["response"]["hits"][0]["result"]["header_image_url"]
        song2img = obj["response"]["hits"][1]["result"]["header_image_url"]
        song3img = obj["response"]["hits"][2]["result"]["header_image_url"]

        song1artists = obj["response"]["hits"][0]["result"]["artist_names"]
        song2artists = obj["response"]["hits"][1]["result"]["artist_names"]
        song3artists = obj["response"]["hits"][2]["result"]["artist_names"]

        return render_template("index.html", artist_name=artist, song1=song1, \
            song2 = song2, song3 = song3, song1img = song1img, song2img = song2img, \
            song3img=song3img, song1artists=song1artists, song2artists=song2artists, song3artists=song3artists)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True,port="8990")