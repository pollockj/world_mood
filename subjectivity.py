from features import word_features, document_features
from nltk.corpus import subjectivity
from nltk.corpus import words as wds
import nltk

##Features
numberWords = 100
words = word_features(subjectivity.words(),numberWords)
f = words + wds.words(fileids='en-basic')

##Data Set

subj = [(sentence,'subj') for sentence in subjectivity.sents(categories='subj')]
obj = [(sentence,'obj') for sentence in subjectivity.sents(categories='obj')]

length = len(subj)
nintyPercent = int(length*.9)

test_tokens = subj[:nintyPercent] + obj[:nintyPercent]
train_tokens = subj[nintyPercent:] + obj[nintyPercent:]

print("Test set length  = " + str(len(test_tokens)))
print("Train set length = " + str(len(train_tokens)))

trainSet = [(document_features(sent,f),category) for (sent,category) in train_tokens]
testSet = [(document_features(sent,f),category) for (sent,category) in test_tokens]


#Train
classifier = nltk.NaiveBayesClassifier.train(trainSet)

print(classifier.show_most_informative_features(5))

#Test
print('Test set accuracy = {:<2}'.format(nltk.classify.accuracy(classifier, testSet)))
print('Train set accuracy = {:<2}'.format(nltk.classify.accuracy(classifier, trainSet)))



