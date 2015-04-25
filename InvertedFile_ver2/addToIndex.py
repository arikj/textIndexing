import sys

from invertedIndex import *
from preprocessing import *


filePath = "../documents/set2/"


def mergeIndex(wordList, index):
	indexFile = invertedIndex()
	indexFile.modifyInvertedList(wordList, index)

def addToIndex(index):
	preprocessText = preprocessing()
	filename = filePath + "doc" + str(index) + ".txt"
	f = open(filename, "r")
	content = f.read()
	wordList = preprocessText.processText(content)
	mergeIndex(wordList, index)
	
	
startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])

for index in range(startIndex, endIndex+1):
	print "Indexing document:", index
	addToIndex(index)