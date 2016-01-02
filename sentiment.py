#Code modified from:
#	http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
#	https://snippetsofcode.wordpress.com/2014/04/28/fast-tutorial-to-nltk-using-python/	

import csv
import nltk
from nltk.tokenize import TweetTokenizer

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = []
    for (word, freq) in wordlist.most_common():
    	word_features.append(word)
    return word_features

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

sts_gold_list = []
with open('sts_gold_v03/sts_gold_tweet.csv') as f:
	f.readline()
	csvfile = csv.reader(f,delimiter=';')
	for row in csvfile:
		text = row[2]
		token_text = TweetTokenizer(preserve_case=False,strip_handles=True, reduce_len=True).tokenize(text)
		rating = row[1]
		if rating == '0':
			rating = 'negative'
		elif rating == '4':
			rating = 'positive'
		sts_gold_list.append([token_text,rating])

word_features = get_word_features(get_words_in_tweets(sts_gold_list))

featuresets = [(document_features(d), c) for (d,c) in sts_gold_list]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(featuresets)
classifier.show_most_informative_features(10)

tweet_list = []
with open('data/stream_Happy_New_Year_Low.csv') as f2:
	f2.readline()
	tweet_file = csv.reader(f2,delimiter=',')
	for row in tweet_file:
		text = row[0]
		token_text = TweetTokenizer(preserve_case=False,strip_handles=True, reduce_len=True).tokenize(text)
		tweet_list.append(token_text)

positive = 0
negative = 0
# sentiment = classifier.classify(document_features(tweet_list[0]))
# if sentiment == 'positive':
# 	positive += 1
# elif sentiment == 'negative':
# 	negative += 1
# else:
# 	print "You shouldn't be here"

# print "sentiment: ", sentiment, "positive = ",positive," negative = ",negative
for tweet in tweet_list:
	sentiment = classifier.classify(document_features(tweet))
	if sentiment == 'positive':
		positive += 1
	elif sentiment == 'negative':
		negative += 1
	else:
		print "You shouldn't be here"
print "positive = ",positive," negative = ",negative
# tweet = 'Your song is annoying'
# token_tweet = TweetTokenizer(preserve_case=False,strip_handles=True, reduce_len=True).tokenize(tweet)
# print classifier.classify(document_features(token_tweet))