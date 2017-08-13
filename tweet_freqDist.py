from nltk.corpus import PlaintextCorpusReader
import nltk
from nltk.tokenize import TweetTokenizer

file = "./twitter_data/tweets.txt"
with open(file) as f:
    raw = f.read()

words = TweetTokenizer().tokenize(raw)
non_features = ['rt','@']
words = [w.lower() for w in words]
words = [w for w in words if w not in non_features]
fdist = nltk.FreqDist(words)
for word, frequency in fdist.most_common(50):
    print(u'{}{}'.format(word, frequency))

