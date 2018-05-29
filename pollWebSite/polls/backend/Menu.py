from . import Util
import time
from datetime import datetime
from datetime import timedelta
from . import Predictor
from . import TwitterFeed
from ..models import CandidatoDto
from django.conf import settings
from multiprocessing import Pool, Lock
import atexit

predictor = Predictor

feed = None

vargasFile = './Tweets/tweets_of_vargas.csv'
petroFile = './Tweets/tweets_of_petro.csv'
calleFile = './Tweets/tweets_of_calle.csv'
duqueFile = './Tweets/tweets_of_duque.csv'
fajardoFile = './Tweets/tweets_of_fajardo.csv'

last3MinutesString = "{} ha tenido en los ultimos 3 minutos {} comentarios positivos y {} comentarios negativos"


def shutdown():
    exit(0)


def exit_handler():
    if feed is not None:
        feed.exit_handler()

def getText(tweets):
    texts = []
    for x in tweets:
        texts.append(x[2])
    return texts

def getAuthors(tweets):
    authors = []
    for x in tweets:
        if x not in authors:
            authors.append(x)
    return authors

def countComments(prediction):
    pos = 0
    neg = 0
    for p in prediction:
        if p == 0:
            neg = neg + 1
        else:
            pos = pos + 1
    return [pos, neg]

def predictSingle(tweets):
    prediction = []
    try:
        return predictor.predict(tweets)
    except Exception as e:
        return []

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


def readFile(candidate):
    tweets = []
    if candidate == 1:
        tweets = Util.readTweetsCsv(vargasFile, 10)
    if candidate == 2:
        tweets = Util.readTweetsCsv(petroFile, 10)
    if candidate == 3:
        tweets = Util.readTweetsCsv(calleFile, 10)
    if candidate == 4:
        tweets = Util.readTweetsCsv(duqueFile, 10)
    if candidate == 5:
        tweets = Util.readTweetsCsv(fajardoFile, 10)

    return tweets


def selectName(candidate):
    name = ""
    if candidate == 1:
        name = "Vargas"
    if candidate == 2:
        name = "Petro"
    if candidate == 3:
        name = "De la Calle"
    if candidate == 4:
        name = "Duque"
    if candidate == 5:
        name = "Fajardo"

    return name


def selectImage(candidate):
    img = ""
    if candidate == 1:
        img = "vargas.jpg"
    if candidate == 2:
        img = "petro.jpg"
    if candidate == 3:
        img = "calle.jpg"
    if candidate == 4:
        img = "duque.jpg"
    if candidate == 5:
        img = "fajardo.jpg"

    return img


def mcd(a, b):
    resto = 0
    while b > 0:
        resto = b
        b = a % b
        a = resto
    return a


def ratio(a, b):
    c = a / mcd(a, b)
    d = b / mcd(a, b)
    return str(int(round(c))) + ':' + str(int(round(d)))


def porcentajes(prediction):
    count = prediction[0] + prediction[1]
    pos = (prediction[0] / count) * 100
    neg = (prediction[1] / count) * 100
    return pos, neg


def createDto(candidate):
    name = selectName(candidate)
    tweets = readFile(candidate)
    veces_mencionado = len(tweets)
    personas_hablando = len(getAuthors(tweets))
    threeMinutesAgo = datetime.now() - timedelta(seconds=180)
    lastTweets = len([x for x in Util.readTweetsCsv(vargasFile, 500) if x[1] >= threeMinutesAgo])
    promedio = lastTweets/3
    img_file = selectImage(candidate)
    prediction = predictSingle(getText(tweets))
    count = countComments(prediction)
    pp, np = porcentajes(count)
    rat = ratio(count[0], count[1])
    candidateDto = CandidatoDto(name,
                                veces_mencionado,
                                personas_hablando,
                                rat,
                                promedio,
                                lastTweets,
                                count[0],
                                pp,
                                count[1],
                                np,
                                img_file)
    return candidateDto, tweets


def getCandidate(text):
    if TwitterFeed.candidates[0].lower() in text.lower() or TwitterFeed.candidates[1].lower() in text.lower():
        return 1

    if TwitterFeed.candidates[2].lower() in text.lower() or TwitterFeed.candidates[3].lower() in text.lower():
        return 2

    if TwitterFeed.candidates[4].lower() in text.lower() or TwitterFeed.candidates[5].lower() in text.lower():
        return 3

    if TwitterFeed.candidates[6].lower() in text.lower() or TwitterFeed.candidates[7].lower() in text.lower():
        return 4

    if TwitterFeed.candidates[8].lower() in text.lower() or TwitterFeed.candidates[9].lower() in text.lower():
        return 5

    return None


def addToCandidate(tweet):
    candidate = getCandidate(tweet[2])
    settings.CANDIDATOS[candidate].veces_mencionado = settings.CANDIDATOS[candidate].veces_mencionado + 1
    settings.CANDIDATOS[candidate].personas_hablando = settings.CANDIDATOS[candidate].personas_hablando + 1
    threeMinutesAgo = datetime.now() - timedelta(seconds=180)
    lastTweets = len([x for x in Util.readTweetsCsv(vargasFile, 1000) if x[1] >= threeMinutesAgo])
    promedio = lastTweets / 3
    settings.CANDIDATOS[candidate].ultimas_menciones = lastTweets
    settings.CANDIDATOS[candidate].promedio = promedio
    prediction = predictSingle(tweet[2])
    count = [settings.CANDIDATOS[candidate].positivos, settings.CANDIDATOS[candidate].negativos]
    if prediction == 1:
        count[0] = count[0] + 1
    else:
        count[1] = count[1] + 1
    pp, np = porcentajes(count)
    settings.CANDIDATOS[candidate].positivos = count[0]
    settings.CANDIDATOS[candidate].positivos_porcentaje = pp
    settings.CANDIDATOS[candidate].negativos = count[1]
    settings.CANDIDATOS[candidate].negativos_porcentaje = np
    rat = ratio(count[0], count[1])
    settings.CANDIDATOS[candidate].ratio = rat

def update():
    while True:
        settings.LOCK.acquire()
        settings.FEED_LOCK.acquire()

        tweets = settings.TWEETS
        for tweet in tweets:
            try:
                print(("funciona"))
                tweetText = '\"%s\",\"%s\",\"%s\"\n' % (tweet[0], tweet[1], tweet[2])
                files = TwitterFeed.getFile(tweet[2])
                if files is not None:
                    for file in files:
                        file.write(tweetText)

                addToCandidate(tweet)
            except Exception as e:
                1
        settings.TWEETS = []
        settings.FEED_LOCK.release()
        settings.LOCK.release()
        time.sleep(30)


def fillDto():
    pool = Pool(5)
    vargasThread = pool.apply_async(createDto, [1])
    petroThread = pool.apply_async(createDto, [2])
    calleThread = pool.apply_async(createDto, [3])
    duqueThread = pool.apply_async(createDto, [4])
    fajardoThread = pool.apply_async(createDto, [5])
    vargasDto, vargasTweets = vargasThread.get()
    petroDto, petroTweets = petroThread.get()
    calleDto, calleTweets = calleThread.get()
    duqueDto, duqueTweets = duqueThread.get()
    fajardoDto, fajardoTweets = fajardoThread.get()

    candidates = [vargasDto, petroDto, calleDto, duqueDto, fajardoDto]
    settings.CANDIDATOS = candidates

    settings.LOCK = Lock()
    settings.FEED_LOCK = Lock()

    atexit.register(exit_handler)
    global feed
    feed = TwitterFeed
    feed.stream()
    Pool(1).apply_async(update, [])



def getDto():
    settings.LOCK.acquire()
    candidatos = settings.CANDIDATOS
    settings.LOCK.release()
    return candidatos





