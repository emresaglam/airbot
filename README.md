# What is airbot?
Airbot is a small API endpoint (with two endpoints at the time of writing) that will accept a geolocation and will return the air quality index of that location.

It's written in few hours work after the Northern California wildfires smoke hit San Francisco and the bay area in October 2017. 

It's designed to answer in the most basic ~~HipChat/~~ Slack format so that it can be used as a ~~HipChat/~~ Slack endpoint for a bot.

No authentication is required to use this API.

# How?

It's designed to be easily deployed on Heroku. You have to define:
- an environment variable AMBEE_TOKEN which contains your API token for AMBEE. You can get it from: https://getambee.com/section/pricing.html
- an environment variable BOT_COMMAND for the command to be invoked to interact with the bot in the channel. (For example: For the command `/aq Istanbul, Turkey` -> `BOT_COMMAND="/aq"`)

# API Endpoints:
~~1. `/aqi/`: accepts POST only. Payload should be HipChat format. Returns basic HipChat message format with colors according to aqi severity.~~
1. `/aqi-slack`: accepts POST only. Payload is Slack's slash command format. Returns a simple message. (Can be improved with Slack shenaningans)
2. `/aqig/<zipcode>`: accepts GET only. Whatever is after the the trailing slash is parsed as the location. Example: /aqig/Istanbul,%20Turkey

# Screenshots

## HipChat
---
HipChat is not supported anymore. WomWomp...

## Slack
![Slack on iOS screenshot](https://i.imgur.com/PaXsvYW.jpg "Slack on iOS screenshot")

# Todo

- There is some error handling at this point. It does not fail very gracefully. 
- ~~Defining the command in the api endpoint. At this point it assumes that the command is /aq and parses accordingly in the Hipchat API. (Never assume)~~