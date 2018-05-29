### Description

This python application is used to see how the people in tweeter is reacting to each presidential candidate for the Colombian elections 2018.
This project provide a web page where the users can see how many people its talking about a candidate, how many positive and negative tweets there is for each one and the average of tweets per minute of each candidate.
This results are only informative and do not pretend to predict the winners neither can be taked as poll for the elections.

### Libraries

In order to execute this program the following libreries are needed:

- Python 3.6

`$ pip install django`

`$ pip install sklearn`

`$ pip install numpy`

`$ pip install scipy`

`$ pip install nltk`

`$ pip install tweepy`

### Enviroment variables
The following env variables must be setted in order to execute the project:

Twitter authentification:

`ckey=XXXXXXXXXX` 

`csecret=XXXXXXXXXX`

`atoken=XXXXXXXXXX`

`asecret=XXXXXXXXXX`

Time (this variable must be set with the time zone of the device, i.e. for UTC−05:00 put -5):

`TZONE=-5`


### Run
Once the requeriments listed behind are met you are able to run this project with the following command:

`$ python manage.py runserver`