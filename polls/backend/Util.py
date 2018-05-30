import csv
import os
from datetime import datetime
from datetime import timedelta

time_zone = None
try:
    tzone = os.getenv('TZONE')
    if tzone is None:
        time_zone = 0
    else:
        time_zone = int(tzone) * -1
except Exception as e:
    print("Bad Time Zone")
    exit(-1)




def readTrainingDataCsv(filename, limit):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, filename)
    ifile = open(file_path, "r", encoding="utf8")
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
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, filename)
    ifile = open(file_path, "r", encoding="utf8")
    reader = csv.reader(ifile, delimiter=",")
    ifileAux = open(file_path, "r", encoding="utf8")
    readerAux = None
    if limit is not -1:
        readerAux = csv.reader(ifileAux, delimiter=",")

    tweets = []
    count = 0
    start = 0
    if limit is not -1:
        row_count = sum(1 for row in readerAux)
        if row_count > limit:
            start = row_count - limit

        for _ in range(start):
            next(reader)
    for row in reader:
        if limit != -1 and count >= limit:
            break
        if len(row) == 3:
            count = count + 1
            timeAdjust = timedelta(hours=time_zone)
            row[1] = datetime.strptime(str(row[1]), '%Y-%m-%d  %H:%M:%S') - timeAdjust
            tweets.append(row)

    ifile.close()
    return tweets
