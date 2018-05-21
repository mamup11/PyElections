import csv


def readTrainingDataCsv(filename, limit):
    ifile = open(filename, "r")
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
