from flask import Flask, url_for, request
import geocoder
import requests
import json
import os

app = Flask(__name__)


def get_air_quality(zipcode):
    air_quality = {}
    g = geocoder.google(zipcode)
    print g.json["city"], g.json["state"]
    lat = g.json["lat"]
    lon = g.json["lng"]
    token = os.environ["BR_TOKEN"]
    url = "https://api.breezometer.com/baqi/?lat={}&lon={}&fields=country_aqi,breezometer_description,country_name&key={}".format(
        lat, lon, token)
    r = requests.get(url)
    air_quality["location"] = "{}, {}".format(g.json["city"], g.json["state"])
    air_quality["raw"] = r.json()
    message = "Air quality index for {} is: {} - {}".format(air_quality["location"], r.json()["country_aqi"], r.json()["breezometer_description"])
    air_quality["message"] = message
    return air_quality


@app.route("/")
def api_root():
    return "Oh hai! This is an API endpoint and this is not the URL you're looking for :)"

@app.route('/aqi/', methods=["POST"])
@app.route('/aqi/<zipcode>', methods=["GET", "POST"])
def aqi(zipcode):
    color = "yellow"
    if request.method == "POST":
        data = request.get_json(force=True, silent=False)
        print data
        zipcode = data["item"]["message"]["message"]
        print zipcode
        zipcode = zipcode[4:]

    message = get_air_quality(zipcode)
    print message
    aqi = message["raw"]["country_aqi"]

    if aqi < 50:
        color = "green"
    elif 50 < aqi < 150:
        color = "yellow"
    elif 150 < aqi < 250:
        color = "red"
    elif 250 < aqi < 1000:
        color = "purple"

    returned = {}
    returned["color"] = color
    returned["message"] = message["message"]
    returned["notify"] = False
    returned["message_format"] = "text"
    returned_json = json.dumps(returned)
    print returned_json
    return returned_json

if __name__ == '__main__':
    app.run()
