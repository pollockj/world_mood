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
addtional_features = ['evil','murder','trump','pro-trump']
# non_features = []
word_features = extract_features(readRaw(featureFile),non_features,addtional_features, numberWords)

#Apply features
length = len(tokensAndLabels)
nintyPercent = int(length*.9)

train_tokens = tokensAndLabels[:nintyPercent]
test_tokens = tokensAndLabels[nintyPercent:]

trainSet = [(document_features(tweet,word_features),emotion) for (tweet,emotion) in train_tokens]
testSet = [(document_features(tweet,word_features),emotion) for (tweet,emotion) in test_tokens]

#Create Train/Test Set


# trainSet,testSet = featureSet[:nintyPercent],featureSet[nintyPercent:]
print("Total set length = {}".format(length))
print("Test set length = {}".format(len(testSet)))



#Train
classifier = nltk.NaiveBayesClassifier.train(trainSet)

print(classifier.show_most_informative_features(5))

#Test
print('Test set accuracy = {:<2}'.format(nltk.classify.accuracy(classifier, testSet)))
print('Train set accuracy = {:<2}'.format(nltk.classify.accuracy(classifier, trainSet)))

errors = []
for (tweet, emotion) in test_tokens:
    guess = classifier.classify(document_features(tweet,word_features))
    if guess != emotion:
        errors.append( (tweet, guess, emotion))
for (tweet, guess, emotion) in errors:
    print('correct={} guess={} tweet={}'.format(emotion, guess, ' '.join(tweet)))