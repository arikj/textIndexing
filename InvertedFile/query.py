from invertedIndex import *
from preprocessing import *

preprocessText = preprocessing()
indexFile = invertedIndex()

queryterms = str(raw_input("Query terms: "))
queryList = preprocessText.processText(queryterms)

indexFile.readFromFile()
docList = []
flag = True

for query in queryList:
	newdocList = indexFile.findDocumentsWithTerm(query)
	if flag == True:
		docList = newdocList
		flag = False
	else:
		convertToSet = set(docList)
		docList = [val for val in newdocList if val in convertToSet]

print docList