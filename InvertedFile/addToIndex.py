import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import *
from invertedIndex import *


filePath = "../documents/set1/"

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

indexFile = invertedIndex()


def mergeIndex(allWordList, index):
	indexFile.readFromFile()
	indexFile.modifyInvertedList(allWordList, index)
	indexFile.writeBackToFile()

def addToIndex(index):
	filename = filePath + "doc" + str(index) + ".txt"
	f = open(filename, "r")
	content = f.read()

	wordList = content.split()
	filteredWords = [w for w in wordList if not w in stopwords.words('english')]

	allWordList = []
	for word in filteredWords:
		word = word.lower()
		word = lemmatizer.lemmatize(word)
		word = stemmer.stem(word);

		if word not in allWordList:
			allWordList.append(word)

	mergeIndex(allWordList, index)
	


startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])

for index in range(startIndex, endIndex+1):
	addToIndex(index)