from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 

consumer_key = "kcK4DoOUoAbxctwduTSAQtzY6"
consumer_secret = "szIHPsPLLMQRBCqnM7l0fFc0f0ORwjEoO8Bc7CbNmVFAxA0Gqp"
access_token = "72737445-Kilwu0V6dtIaJo0P7BibaTRSQBTUwxrutkdQgdQZn"
access_token_secret = "GYSuHSj8tmqiX9Mz3XwAKJ7AnC7lkMuygJxGa7aTqHTBp"
 
class StdOutListener(StreamListener):
 
    def on_data(self, data):
        print data
        return True
 
    def on_error(self, status):
        print status
 
if __name__ == '__main__':
 
    listener = StdOutListener()
    auth_handler = OAuthHandler(consumer_key, consumer_secret)
    auth_handler.set_access_token(access_token, access_token_secret)
    stream = Stream(auth_handler, listener)
 
    while True:
        try:
            stream.filter(track=['Mourinho'])
        except:
            continue
