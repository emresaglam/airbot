# What is airbot?
Airbot is a small API endpoint (with one endpoint at the time of writing) that will accept a geolocation and will return the air quality index of that location.

It's written in few hours work after the Northern California wildfires smoke hit San Francisco and the bay area. 

It's designed to answer in the most basic HipChat format so that it can be used as a HipChat endpoint for a bot.

No authentication is required to use this API.

# How?

It's designed to be easily deployed on Heroku. You have to define an environment variable BR_TOKEN which contains your API token for Breezometer. 
You can get it from: https://developers.breezometer.com

# Todo

- There is absolutely no error handling at this point. It will not fail gracefully.
- There is no input sanitation. It should fail after geocoder library return fails. 
