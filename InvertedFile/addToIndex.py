import sys

from invertedIndex import *
from preprocessing import *



filePath = "../documents/set1/"

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

indexFile = invertedIndex()
preprocessText = preprocessing()


def mergeIndex(allWordList, index):
	indexFile.readFromFile()
	indexFile.modifyInvertedList(allWordList, index)
	indexFile.writeBackToFile()

def addToIndex(index):
	filename = filePath + "doc" + str(index) + ".txt"
	f = open(filename, "r")
	content = f.read()
	allWordList = preprocessText.processText(content)
	mergeIndex(allWordList, index)
	


startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])

for index in range(startIndex, endIndex+1):
	print "Analysing document:", index
	addToIndex(index)