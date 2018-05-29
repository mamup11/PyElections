from __future__ import unicode_literals
import tweepy
import os
import atexit
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from django.conf import settings
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

vargasFile = None
petroFile = None
calleFile = None
duqueFile = None
fajardoFile = None


def doAuth():
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    return auth


def getFile(text):
    files = []
    if candidates[0].lower() in text.lower() or candidates[1].lower() in text.lower():
        files.append(vargasFile)

    if candidates[2].lower() in text.lower() or candidates[3].lower() in text.lower():
        files.append(petroFile)

    if candidates[4].lower() in text.lower() or candidates[5].lower() in text.lower():
        files.append(calleFile)

    if candidates[6].lower() in text.lower() or candidates[7].lower() in text.lower():
        files.append(duqueFile)

    if candidates[8].lower() in text.lower() or candidates[9].lower() in text.lower():
        files.append(fajardoFile)

    if len(files) > 0:
        return files
    return None


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


def stream():
    auth = doAuth()
    global vargasFile
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, './Tweets/tweets_of_vargas.csv')
    vargasFile = open(file_path, 'a')
    global petroFile
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, './Tweets/tweets_of_petro.csv')
    vargasFile = open(file_path, 'a')
    global calleFile
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, './Tweets/tweets_of_calle.csv')
    vargasFile = open(file_path, 'a')
    global duqueFile
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, './Tweets/tweets_of_duque.csv')
    vargasFile = open(file_path, 'a')
    global fajardoFile
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, './Tweets/tweets_of_fajardo.csv')
    vargasFile = open(file_path, 'a')
    global twitterStream
    twitterStream = Stream(auth, Listener(), tweet_mode='extended')
    twitterStream.filter(track=candidates, async=True)


def exit_handler():
    global twitterStream
    if twitterStream is not None:
        twitterStream.disconnect()
    if vargasFile is not None:
        vargasFile.close()
    if petroFile is not None:
        petroFile.close()
    if calleFile is not None:
        calleFile.close()
    if duqueFile is not None:
        duqueFile.close()
    if fajardoFile is not None:
        fajardoFile.close()

atexit.register(exit_handler)
