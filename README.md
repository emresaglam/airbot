# What is airbot?
Airbot is a small API endpoint (with three endpoints at the time of writing) that will accept a geolocation and will return the air quality index of that location.

It's written in few hours work after the Northern California wildfires smoke hit San Francisco and the bay area in October 2017. 

It's designed to answer in the most basic HipChat/Slack format so that it can be used as a HipChat/Slack endpoint for a bot.

No authentication is required to use this API.

# How?

It's designed to be easily deployed on Heroku. You have to define:
- an environment variable BR_TOKEN which contains your API token for Breezometer. You can get it from: https://developers.breezometer.com
- an environment variable ROOM_NAME for a room name for HipChat to be whitelisted. (To be only called from that room name, all other rooms will advertise ROOM_NAME)

# API Endpoints:
1. `/aqi/`: accepts POST only. Payload should be HipChat format. Returns basic HipChat message format with colors according to aqi severity.
2. `/aqi-slack`: accepts POST only. Payload is Slack's slash command format. Returns a simple message. (Can be improved with Slack shenaningans)
3. `/aqig/<zipcode>`: accepts GET only. Whatever is after the the trailing slash is parsed as the location. Example: /aqig/Istanbul,%20Turkey

# Todo

- There is some error handling at this point. It does not fail very gracefully. 
- If no ROOM_NAME is defined, should stop whitelisting.
- Should accept multiple room names (Maybe a comma separated ROOM_NAME variable?)
- Defining the command in the api endpoint. At this point it assumes that the command is /aq and parses accordingly in the Hipchat API. (Never assume)