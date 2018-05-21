from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
import TextProcessing
import Util

# build a Pipeline object with the better parameters
pipeline = Pipeline([
    ('vect', CountVectorizer(
            analyzer='word',
            tokenizer=TextProcessing.tokenize,
            lowercase=True,
            stop_words=TextProcessing.spanish_stopwords,
            min_df=50,
            max_df=1.9,
            ngram_range=(1, 1),
            max_features=1000
            )),
    ('cls', LinearSVC(C=.2, loss='squared_hinge',max_iter=1000,multi_class='ovr',
                      random_state=None,
                      penalty='l2',
                      tol=0.0001
                      )),
])


trainingContent, trainingPolarity = Util.readTrainingDataCsv("Training Data/2clases_es_generaltassisol_pub.csv", -1)

# we fit the pipeline with the TASS corpus
pipeline.fit(trainingContent, trainingPolarity)


def predict(tweet):

    prediction = pipeline.predict(tweet)
    i = 0
    while i < len(prediction):
        print("Predicted: " + str(prediction[i]) + " for twit: " + tweet[i])
        i = i + 1;
    return prediction


#tweets = [
#        "#Perfil @German_Vargas \"es el hombre mejor preparado para asumir la presidencia\", asegura su esposa Luz María Zapata http://ow.ly/rnsy30k5a96 "

#    ]
#predict(tweets)
