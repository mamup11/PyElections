from __future__ import unicode_literals
import tweepy
import os
import atexit
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from django.conf import settings
import threading
from multiprocessing import Lock

## Codigo del Listener sacado de: https://github.com/manugarri/tweets_map

candidates = ["german vargas", "@German_Vargas",
              "gustavo petro", "@petrogustavo",
              "humberto de la calle", "@DeLaCalleHum",
              "ivan duque", "@IvanDuque",
              "sergio fajardo", "@sergio_fajardo"]

query = "german vargas OR @German_Vargas OR gustavo petro OR @petrogustavo OR " \
        "humberto de la calle OR @DeLaCalleHum OR ivan duque OR @IvanDuque OR " \
        "sergio fajardo OR @sergio_fajardo"

ckey = os.getenv('ckey')
csecret = os.getenv('csecret')
atoken = os.getenv('atoken')
asecret = os.getenv('asecret')

DEBUG = os.getenv('P2DEBUG')

twitterStream = None


def doAuth():
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    return auth


def authorFilter(user):
    if str(user).lower().__contains__(candidates[1].lower()):
        return True
    if str(user).lower().__contains__(candidates[3].lower()):
        return True
    if str(user).lower().__contains__(candidates[5].lower()):
        return True
    if str(user).lower().__contains__(candidates[7].lower()):
        return True
    if str(user).lower().__contains__(candidates[9].lower()):
        return True
    return False


class Listener(StreamListener):

    def on_status(self, status):#(self, data):
        # Twitter returns data in JSON format - we need to decode it first

        if status.geo is not None:
            location = status.geo
        else:
            location = '[,]'
        text = None
        try:
            if status.extended_tweet is not None:
                text = status.extended_tweet["full_text"].replace('\n', ' ')
        except Exception as e:
            try:
                if status.quoted_status.extended_tweet is not None:
                    text = status.quoted_status.extended_tweet["full_text"].replace('\n', ' ')
            except Exception as e:
                try:
                    if status.retweeted_status.extended_tweet is not None:
                        text = status.retweeted_status.extended_tweet["full_text"].replace('\n', ' ')
                except Exception as e:
                    1
        if text is not None:
            user = '@' + status.user.screen_name
            if authorFilter(str(user)):
                return True
            settings.FEED_LOCK.acquire()
            created = status.created_at
            tweet = [user, created, text]
            settings.TWEETS.append(tweet)
            settings.FEED_LOCK.release()
        return True

    def on_error(self, status):
        print(status)


def parse(tweets):
    for tweet in tweets:
        print(tweet.text)
    return tweets


def search(date):
    api = tweepy.API(doAuth())
    tweets = api.search(q=query, count=500, tweet_mode="extended")#, until=date)
    print(candidates.__str__())
    dataObject = parse(tweets)
    return dataObject


def stream_daemon():
    while True:
        try:
            auth = doAuth()
            global twitterStream
            twitterStream = Stream(auth, Listener(), tweet_mode='extended')
            twitterStream.filter(track=candidates)
        except Exception as e:
            print("Excepcion en stream_daemon: \n" + e.__str__())

def stream():
    d = threading.Thread(name='daemon', target=stream_daemon)
    d.setDaemon(True)
    d.start()


def exit_handler():
    global twitterStream
    if twitterStream is not None:
        twitterStream.disconnect()

atexit.register(exit_handler)
