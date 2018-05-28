# twitterchannels

Simple example to show the use of websockets to update a webpage view when new data is gathered.

In this example you can listen the tweets sent from a map area, plotting the coordinates of the ones that are geolocated.

Once the user sets the map area a message is sent from the web browser to the server. The server starts a streaming channel that asynchronously sends the tweets received to the map.

## Check this documentation for background information

- [WebSockets](https://www.websocket.org/aboutwebsocket.html)
- WebSockets for Django: [Django Channels](https://channels.readthedocs.io/en/latest/)
- Twitter streaming: [Streaming With Tweepy](http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html)
- Map manipulation: [Leaflet](https://leafletjs.com/)
