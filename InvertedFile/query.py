from invertedIndex import *
from preprocessing import *
from math import log10

topResult = 10

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))

print "1. Search by terms query\n2. Search by phrase query\n3. Ranking of documents based on query"
option = int(raw_input("Select an option: "))

if option == 1:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Query terms: "))
	queryList = preprocessText.processText(queryterms)

	indexFile.readFromFile()
	docList = []
	flag = True

	for query in queryList.words:
		newdocList = indexFile.findDocumentsWithTerm(query)
		newdoc = newdocList.document

		if flag == True:
			docList = newdoc
			flag = False
		else:
			convertToSet = set(docList)
			docList = [val for val in newdoc if val in convertToSet]

	print docList

elif option == 2:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Phrase terms: "))
	queryList = preprocessText.processText(queryterms)

	indexFile.readFromFile()
	docList = []
	posList = []
	flag = True

	for query in queryList.words:
		newdocList = indexFile.findDocumentsWithTerm(query)

		if flag == True:
			docList = newdocList.document
			for k in range(0, len(newdocList.document)):
				posList.append(newdocList.posList[k])
			flag = False

		else:
			removeElem = []
			for k in range(0,len(docList)):
				if docList[k] in newdocList.document:
					matchIndex = newdocList.document.index(docList[k])
					newVector = []
					for i in range(0, len(posList[k])):
						found = False
						for j in range(0, len(newdocList.posList[matchIndex])):
							if posList[k][i] + 1 == newdocList.posList[matchIndex][j]:
								found = True
								break
						if found == True:
							newVector.append(posList[k][i]+1)
	
					if len(newVector) != 0:
						posList[k] = newVector		

					else:
						removeElem.append(k)
				else:
					removeElem.append(k)

			copyDoc = []
			copyPos = []

			for k in range(0, len(docList)):
				if k not in removeElem:
					copyDoc.append(docList[k])
					copyPos.append(posList[k])

			docList = copyDoc
			posList = copyPos

	print docList


elif option == 3:
	preprocessText = preprocessing()
	indexFile = invertedIndex()

	queryterms = str(raw_input("Query terms: "))
	queryList = preprocessText.processText(queryterms)

	indexFile.readFromFile()

	scoreDoc = {}
	for query in queryList.words:
		newdocList = indexFile.findDocumentsWithTerm(query)

		for k in range(0, len(newdocList.document)):
			if newdocList.document[k] not in scoreDoc:
				scoreDoc[newdocList.document[k]] = computeScore(newdocList.frequency[k], indexFile.totalDoc, len(newdocList.document))

			else:
				scoreDoc[newdocList.document[k]] += computeScore(newdocList.frequency[k], indexFile.totalDoc, len(newdocList.document))

	newList = sorted(scoreDoc.iteritems(), key=lambda x:-x[1])[:min(topResult, len(scoreDoc))]

	for value in newList:
		print  "Document: " + str(value[0]) + " score: " + str(value[1])

else:
	print "No such option"