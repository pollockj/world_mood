import nltk
from nltk.tokenize import TweetTokenizer
import emoji_list as emoji#Found a list of emoji https://github.com/vincentmwong/emoji_list

def document_features(document,word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def readRaw(file):
    with open(file) as f:
         return f.read()


def word_features(raw_data,non_features,additional_features,N,verbose=False):
    words = TweetTokenizer().tokenize(raw_data)
    words = [w.lower() for w in words]
    words = [w for w in words if w not in non_features]
    words = [w for w in words if w.isalpha()]
    fdist = nltk.FreqDist(words)
    if verbose:
        for word, frequency in fdist.most_common(N):
            print(u'{}  {}'.format(word, frequency))
    return list(set(list(fdist)[:N] + additional_features))

def emoji_features():
    return emoji.all_emoji

def punctuation_features():
    return ['!','?']

