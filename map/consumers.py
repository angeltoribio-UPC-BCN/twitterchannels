import json

from channels.generic.websocket import WebsocketConsumer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from django.conf import settings



class MyListener(StreamListener):

    def __init__(self, consumer):
        self.consumer = consumer

    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['coordinates']:
            self.consumer.send(text_data=json.dumps({
                'message': {
                    'id': tweet['id_str'],
                    'c0': str(tweet['coordinates']['coordinates'][0]),
                    'c1': str(tweet['coordinates']['coordinates'][1]),
                    'text': tweet['text'],
                    "created_at": tweet['created_at'],
                }
            }))
        return True

    def on_error(self, status):
        # print('status:%d' % status)
        return True


class MapConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

        twitter_stream = Stream(auth, MyListener(self))
        dx = 1.0
        dy = 1.0
        # [SWlongitude, SWLatitude, NElongitude, NELatitude]
        (SWLo,SWLa,NELo,NELa)= (message[1]-dx, message[0]-dy, message[1]+dx, message[0]+dy)
        twitter_stream.filter(locations=[SWLo,SWLa,NELo,NELa], async=True)
