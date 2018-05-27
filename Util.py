import csv
from datetime import datetime
from datetime import timedelta

def readTrainingDataCsv(filename, limit):
    ifile = open(filename, "r", encoding="utf8")
    reader = csv.reader(ifile, delimiter=",")

    content = []
    polarity = []
    pos = 0
    neg = 0
    for row in reader:
        if limit != -1 and pos >= limit/2 and neg >= limit/2:
            break
        if len(row) == 2:
            if row[1] == 'neg':
                if limit == -1 or neg <= limit/2:
                    neg = neg + 1
                    polarity.append(0)

                    content.append(row[0])
            else:
                if limit == -1 or pos <= limit/2:
                    pos = pos + 1
                    polarity.append(1)
                    content.append(row[0])

    ifile.close()
    return content, polarity


def readTweetsCsv(filename, limit):
    ifile = open(filename, "r", encoding="utf8")
    reader = csv.reader(ifile, delimiter=",")
    ifileAux = open(filename, "r", encoding="utf8")
    readerAux = csv.reader(ifileAux, delimiter=",")

    tweets = []
    count = 0
    start = 0
    row_count = sum(1 for row in readerAux)
    if row_count > limit:
        start = row_count - limit

    for _ in range(start):
        next(reader)
    for row in reader:
        if limit != -1 and count == limit:
            break
        count = count + 1
        timeAdjust = timedelta(hours=5)
        try:
            row[1] = datetime.strptime(str(row[1]), '%Y-%m-%d  %H:%M:%S') - timeAdjust
            tweets.append(row)
        except Exception as e:
            1


    ifile.close()
    return tweets
