import nltk
from . import Util as util
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer

## Codigo sacado de: http://blog.manugarri.com/sentiment-analysis-in-spanish/
nltk.download('stopwords')
nltk.download('punkt')

spanish_stopwords = stopwords.words('spanish')


non_words = list(punctuation)
non_words.extend(['¿', '¡', '%', '“'])
non_words.extend(map(str, range(10)))

words_root = SnowballStemmer('spanish')


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    text = ''.join([w for w in text if w not in non_words])
    tokens = word_tokenize(text)

    # stem
    try:
        stems = stem_tokens(tokens, words_root)
    except Exception as e:
        print(e)
        print(text)
        stems = ['']
    return stems


vectorizer = CountVectorizer(
    analyzer='word',
    tokenizer=tokenize,
    lowercase=True,
    stop_words=spanish_stopwords)


from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# LinearSVC() es el clasificador

pipeline = Pipeline([
    ('vect', vectorizer),
    ('cls', LinearSVC()),
])

# {'vect__min_df': 0.01,
# 'cls__max_iter': 500,
# 'vect__ngram_range': (1, 2),
# 'cls__C': 0.7,
# 'vect__max_df': 0.5,
# 'cls__loss': 'squared_hinge',
# 'vect__max_features': 500}
# Aqui definimos el espacio de parámetros a explorar
parameters = {
    'vect__max_df': (0.5, 1.9),
    'vect__min_df': (0.01, 0.02, 0.05),
    'vect__max_features': (500, 1000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigramas or bigramas
    'cls__C': (0.2, 0.5, 0.7),
    'cls__loss': ('hinge', 'squared_hinge'),
    'cls__max_iter': (500, 1000)
}


def parameterSearch():
    tweetsContent, tweetsPolarity = util.readcsv("Training Data/2clases_es_generaltassisol_pub.csv", 500)

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(tweetsContent, tweetsPolarity)

    tweet = ["Aquí os dejo un video con algunas reacciones del público al salir de ver Grease!! "
            "Muchisimas gracias a todos!!! http://t.co/ytJUWcLn", "Día de la Mujer/3. La violencia machista y la brecha salarial "
            "lastran la igualdad en la UE  http://t.co/mWmwrRO4 via @el_pais"]

    prediction2 = pipeline.predict(tweet)
    print(prediction2)


def parseTASSDataset():
    corpus = ET.parse("Training Data/general-train-tagged-3l.xml")
    tweets = corpus.getroot()
    count = 0
    for tweet in tweets.findall("tweet"):
        count = count + 1

    print(count)

    corpus = ET.parse("Training Data/intertass-train-tagged.xml")
    tweets = corpus.getroot()
    count2 = 0
    for tweet in tweets.findall("tweet"):
        count2 = count2 + 1

    print(count2)
    print(count+count2)


    return


#parseTASSDataset()
