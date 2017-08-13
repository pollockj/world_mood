import nltk
from nltk.tokenize import TweetTokenizer

def document_features(document,word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def readRaw(file):
    with open(file) as f:
         return f.read()


def extract_features(raw_data,non_features,additional_features,N,verbose=False):
    words = TweetTokenizer().tokenize(raw_data)
    words = [w.lower() for w in words]
    words = [w for w in words if w not in non_features]
    fdist = nltk.FreqDist(words)
    if verbose:
        for word, frequency in fdist.most_common(N):
            print(u'{}  {}'.format(word, frequency))
    return set(list(fdist)[:N] + additional_features)

# if __name__ == "__main__":
#     file = "./twitter_data/tweets.txt"
#     raw = readRaw(file)
#     non_features = ['rt', '@']
#     extract_features(raw,non_features,50,False)

