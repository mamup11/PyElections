import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer

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


# Aqui definimos el espacio de parámetros a explorar
parameters = {
    'vect__max_df': (0.5, 1.9),
    'vect__min_df': (10, 20,50),
    'vect__max_features': (500, 1000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigramas or bigramas
    'cls__C': (0.2, 0.5, 0.7),
    'cls__loss': ('hinge', 'squared_hinge'),
    'cls__max_iter': (500, 1000)
}

import csv


def readcsv(filename):
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=",")

    content = []
    polarity = []

    for row in reader:
        if len(row) == 2:
            content.append(row[0])
            if row[1] == 'neg':
                polarity.append(0)
            else:
                polarity.append(1)

    ifile.close()
    return content, polarity


twitsContent, twitsPolarity = readcsv("Training Data/2clases_es_generaltassisol_pub.csv")


grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, scoring='roc_auc')
grid_search.fit(twitsContent, twitsPolarity)
