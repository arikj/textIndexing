from invertedIndex import *
from preprocessing import *
from math import log10


def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))

print "1. Search by terms query\n2. Search by phrase query\n3. Ranking of documents based on query"
option = int(raw_input("Select an option: "))

if option == 1:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Query terms: "))
	queryList = preprocessText.processText(queryterms)

	docList = []
	flag = True
	docList = indexFile.findDocumentsWithTerm(queryList.words)
	print docList

elif option == 2:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Phrase terms: "))
	queryList = preprocessText.processText(queryterms)

	docList = indexFile.findDocumentsWithPhrase(queryList.words)
	print docList


elif option == 3:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Query terms: "))
	topResult = int(raw_input("Number of documents: "))

	queryList = preprocessText.processText(queryterms)

	newList = indexFile.findTopKDocuments(queryList.words, topResult)

	for value in newList:
		print  "Document: " + str(value[0]) + " score: " + str(value[1])

else:
	print "No such option"