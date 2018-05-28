import json
from django.conf import settings
from channels.generic.websocket import WebsocketConsumer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyListener(StreamListener):

    def __init__(self, consumer):
        self.consumer = consumer

    def on_data(self, data):
        tweet = json.loads(data)
        # Send message to connected browser
        if 'coordinates' in tweet and tweet['coordinates']:
            self.consumer.send(text_data=json.dumps({
                'type': 'tweet',
                'coordinates': 'true',
                'message': {
                    'lng': str(tweet['coordinates']['coordinates'][0]),
                    'lat': str(tweet['coordinates']['coordinates'][1]),
                    'text': '<strong>%s</strong>: %s'%(tweet['user']['name'],tweet['text']),
                }
            }))
        else:
            self.consumer.send(text_data=json.dumps({
                'type': 'tweet',
                'coordinates': 'false',
                'message': {
                    'text': '<strong>%s</strong>: %s'%(tweet['user']['name'],tweet['text']),
                }
            }))

        return True

    def on_error(self, status):
        self.consumer.send(text_data=json.dumps({
            'type': 'control',
            'action': 'error',
            'message': status,
        }))
        return True


class MapConsumer(WebsocketConsumer):
    twitter_stream = None
    auth = None

    def connect(self):
        self.accept()
        self.auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        self.auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

    def disconnect(self, close_code):
        if self.twitter_stream is not None:
            self.twitter_stream.disconnect()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'listen':
            message = text_data_json['message']
            self.twitter_stream = Stream(self.auth, MyListener(self))

            # Create a new stream and filter by bounding box
            # A new thread (async) is required not to block this HTTP transaction
            # [SWlongitude, SWLatitude, NElongitude, NELatitude]
            self.twitter_stream.filter(locations=message, async=True)
        elif text_data_json['type'] == 'stop':
            self.twitter_stream.disconnect()
