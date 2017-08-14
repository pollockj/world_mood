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
    return list(set(list(fdist)[:N] + additional_features))

def emoji_features():
    e = []
    c = 128512
    ##Face Emojis
    for i in range(79):
        # print(chr(c))
        e.append(chr(c))
        c += 1

    #Transportation Emojis
    c = 128639
    for i in range(70):
        # print(chr(c))
        e.append((chr(c)))
        c += 1

    #Punctuation Emoji
    c = 10067
    e.append(chr(c))
    e.append(chr(c+1))
    e.append(chr(c+2))
    e.append(chr(c+4))

    #Love Emoji
    c = 128139
    for i in range(21):
        # print(chr(c))
        e.append(chr(c))
        c += 1

    return e

# def hashtag_features(raw_data):


# if __name__ == "__main__":
#     e = emoji_features()
#     print(e)
#     file = "./twitter_data/tweets.txt"
#     raw = readRaw(file)
#     non_features = ['rt', '@']
#     extract_features(raw,non_features,50,False)

