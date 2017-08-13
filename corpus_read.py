from nltk.corpus import PlaintextCorpusReader

corpus_root = './twitter_data'
wordlists = PlaintextCorpusReader(corpus_root, '.*\.txt')
id = wordlists.fileids()[0]

print(wordlists.words(id))