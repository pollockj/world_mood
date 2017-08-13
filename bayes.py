from load_set import loadSet
from features import *
import nltk

setFile = "./data/compressed.csv"

includeEmotions = ["Happy", "Anger/Upset"]
tokensAndLabels = loadSet(setFile,includeEmotions)

##Extract features
numberWords = 1000
featureFile = "./twitter_data/tweets.txt"
non_features= ['@','rt']
word_features = extract_features(readRaw(featureFile),non_features,numberWords)

#Apply features
featureSet = [(document_features(tweet,word_features),emotion) for (tweet,emotion) in tokensAndLabels]

#Create Train/Test Set
length = len(featureSet)
nintyPercent = int(length*.9)
trainSet,testSet = featureSet[:nintyPercent],featureSet[nintyPercent:]

#Train
classifier = nltk.NaiveBayesClassifier.train(trainSet)

print(classifier.show_most_informative_features(5))

#Test
print(nltk.classify.accuracy(classifier, testSet))