from flask import Flask, url_for, request
from werkzeug.datastructures import ImmutableMultiDict
import geocoder
import requests
import json
import os

app = Flask(__name__)

def get_air_quality(zipcode):
	g = geocoder.google(zipcode)
	lat = g.json["lat"]
	lon = g.json["lng"]
	token = os.environ["BR_TOKEN"]
	url = "https://api.breezometer.com/baqi/?lat={}&lon={}&fields=country_aqi,breezometer_description&key={}".format(lat,lon,token)
	r = requests.get(url)
	message = "Air quality index is: {} - {}".format(r.json()["country_aqi"], r.json()["breezometer_description"])
	print message
	return message

@app.route("/")
def api_root():
	return 'Oh hai!'

@app.route('/aqi/', methods=["POST"])
def aqi():
	data = request.form
	datadict = list(data)
	print datadict[0]
	received_message = json.loads(datadict[0])
	zipcode = received_message["item"]["message"]
	print zipcode
	zipcode = zipcode[4:]
	message = get_air_quality(zipcode)
	returned = {}
	returned["color"] = "green"
	returned["message"] = message
	returned["notify"] = False
	returned["message_format"] = "text"
	returned_json = json.dumps(returned)
	print returned_json
	return returned_json

	
if __name__ == '__main__':
    app.run()
