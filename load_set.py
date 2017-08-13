import csv
from nltk.tokenize import TweetTokenizer
from nltk import bigrams
def loadSet(file, includeEmotions):
    #Loads classified tweets from csv file (2 columns "Text,Emotion")
    #Returns list of tuples with tokenized text (list) and emotion
    with open(file) as f:
        data = []
        reader = csv.DictReader(f)
        for line in reader:
            if line["Emotion"] in includeEmotions:
                text = TweetTokenizer().tokenize(line["Text"].lower())
                # text = addBigrams(text)
                data.append((text,line["Emotion"]))

        return data

def addBigrams(tokenized):
    data = []
    for b in bigrams(tokenized):
        data.append(' '.join(b))
    return data + tokenized

# if __name__ == "__main__":
#     l = ['i','like','apples']
#     print(addBigrams(l))

