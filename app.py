from flask import Flask, request
import geocoder
import requests
import json
import os

app = Flask(__name__)


def get_air_quality(zipcode):
    '''
    Get the location data (as zipcode or free form). Use geocoder to lookup from google
    convert it to lat/lon and feed it to Breezometer API to get the AQI and some more data.
    :param zipcode: 
    :return: 
    '''
    token = os.environ["BR_TOKEN"]
    air_quality = {}
    g = geocoder.google(zipcode)
    if g.status == "OK":
        lat = g.json.get("lat")
        lon = g.json.get("lng")
        url = "https://api.breezometer.com/baqi/?lat={}&lon={}&fields=country_aqi,breezometer_description,country_name&key={}".format(lat, lon, token)
        try:
            r = requests.get(url)
            air_quality["location"] = "{}, {}".format(g.json["city"], g.json["state"])
            air_quality["raw"] = r.json()
            message = "Air quality index for {} is: {} - {}".format(air_quality["location"], r.json()["country_aqi"],
                                                                    r.json()["breezometer_description"])
            air_quality["message"] = message
            air_quality["query_status"] = "OK"
        except requests.exceptions.RequestException as e:
            air_quality["message"] = "{}".format(e)
    else:
        air_quality["query_status"] = "ERROR"

    return air_quality


@app.route('/')
def api_root():
    return "Oh hai! This is an API endpoint and this is not the URL you're looking for :)"


@app.route('/aqi/', methods=["POST"])
def aqi():
    '''
    The payload for the POST request must follow the HipChat 
    room_message webhook format: https://www.hipchat.com/docs/apiv2/webhooks#room_message
    
    It returns a basic HipChat message with different colors depending on the air quality
    :return: 
    '''
    aqiroom = os.environ["ROOM_NAME"]
    color = "yellow"
    returned = {}
    message = {}
    data = request.get_json(force=True, silent=False)
    print data
    if data["item"]["room"]["name"] != aqiroom:
        message["message"] = "This command doesn't work in this room. Please visit '{}'".format(aqiroom)
        color = "red"
    else:
        zipcode = data["item"]["message"]["message"]
        zipcode = zipcode[4:]

        message = get_air_quality(zipcode)
        if message["query_status"] == "OK":
            aqi = message["raw"]["country_aqi"]

            if aqi < 50:
                color = "green"
            elif 50 < aqi < 150:
                color = "yellow"
            elif 150 < aqi < 250:
                color = "red"
                color = "red"
            elif 250 < aqi < 1000:
                color = "purple"
        else:
            message["message"] = "This location is not recognized"

    returned["color"] = color
    returned["message"] = message["message"]
    returned["notify"] = False
    returned["message_format"] = "text"
    returned_json = json.dumps(returned)
    return returned_json


@app.route("/aqig/<zipcode>", methods=["GET"])
def aqig(zipcode):
    '''
    Creates a GET api endpoint where we can query this feeding the parameter at the end of the URL
    Example: http://127.0.0.1:8000/aqig/Istanbul
    :param zipcode: 
    :return: 
    '''
    returned = {}
    message = get_air_quality(zipcode)
    if message["query_status"] == "OK":
        aqi = message["raw"]["country_aqi"]
        color = "green"
    else:
        message["message"] = "This location is not recognized"
        color = "red"
    returned["color"] = color
    returned["message"] = message["message"]
    returned["notify"] = False
    returned["message_format"] = "text"
    returned_json = json.dumps(returned)
    return returned_json

if __name__ == '__main__':
    app.run()
