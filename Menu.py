import Util
from datetime import datetime
from datetime import timedelta
import Predictor
import TwitterFeed

predictor = Predictor

vargasFile = './Tweets/tweets_of_vargas.csv'
petroFile = './Tweets/tweets_of_petro.csv'
calleFile = './Tweets/tweets_of_calle.csv'
duqueFile = './Tweets/tweets_of_duque.csv'
fajardoFile = './Tweets/tweets_of_fajardo.csv'

last3MinutesString = "{} ha tenido en los ultimos 3 minutos {} comentarios positivos y {} comentarios negativos"

def shutdown():
    exit(0)


def getText(tweets):
    texts = []
    for x in tweets:
        texts.append(x[2])
    return texts


def countComments(prediction):
    pos = 0
    neg = 0
    for p in prediction:
        if p == 0:
            neg = neg + 1
        else:
            pos = pos + 1
    return [pos, neg]


def predict(vargasTweets, petroTweets, calleTweets, duqueTweets, fajardoTweets):
    prediction = []
    try:
        prediction.append(predictor.predict(vargasTweets))
    except Exception as e:
        prediction.append([])
    try:
        prediction.append(predictor.predict(petroTweets))
    except Exception as e:
        prediction.append([])
    try:
        prediction.append(predictor.predict(calleTweets))
    except Exception as e:
        prediction.append([])
    try:
        prediction.append(predictor.predict(duqueTweets))
    except Exception as e:
        prediction.append([])
    try:
        prediction.append(predictor.predict(fajardoTweets))
    except Exception as e:
        prediction.append([])

    return prediction


def predictLast3Minutes():
    threeMinutesAgo = datetime.now() - timedelta(seconds=180)
    vargasTweets = [ x for x in Util.readTweetsCsv(vargasFile, 500) if x[1] >= threeMinutesAgo]
    petroTweets = [ x for x in Util.readTweetsCsv(petroFile, 500) if x[1] >= threeMinutesAgo]
    calleTweets = [ x for x in Util.readTweetsCsv(calleFile, 500) if x[1] >= threeMinutesAgo]
    duqueTweets = [ x for x in Util.readTweetsCsv(duqueFile, 500) if x[1] >= threeMinutesAgo]
    fajardoTweets = [ x for x in Util.readTweetsCsv(fajardoFile, 500) if x[1] >= threeMinutesAgo]

    prediction = predict(getText(vargasTweets), getText(petroTweets),
            getText(calleTweets), getText(duqueTweets),
            getText(fajardoTweets))

    count = countComments(prediction[0])
    print(last3MinutesString.format("Vargas", count[0], count[1]))
    count = countComments(prediction[1])
    print(last3MinutesString.format("Petro", count[0], count[1]))
    count = countComments(prediction[2])
    print(last3MinutesString.format("De la Calle", count[0], count[1]))
    count = countComments(prediction[3])
    print(last3MinutesString.format("Duque", count[0], count[1]))
    count = countComments(prediction[4])
    print(last3MinutesString.format("Fajardo", count[0], count[1]))


def predictLast7Days():
    feed = TwitterFeed
    date = datetime.now().strftime("%Y-%m-%d")
    search = feed.search(date)
    if search is not None:
        1
