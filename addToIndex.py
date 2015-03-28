import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import *


filePath = "./documents/set1/"

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def addToIndex(index):
	filename = filePath + "doc" + str(index) + ".txt"
	f = open(filename, "r")
	content = f.read()

	wordList = content.split()
	filteredWords = [w for w in wordList if not w in stopwords.words('english')]

	frequency = {}
	for word in filteredWords:
		word = word.lower()
		word = lemmatizer.lemmatize(word)
		word = stemmer.stem(word);

		if word in frequency:
			frequency[word] += 1
		else:
			frequency[word] = 1

	


startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])

for index in range(startIndex, endIndex+1):
	addToIndex(index)