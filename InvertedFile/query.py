from invertedIndex import *
from preprocessing import *

preprocessText = preprocessing()
indexFile = invertedIndex()

queryterms = str(raw_input("Query terms: "))
queryList = preprocessText.processText(queryterms)

indexFile.readFromFile()

for query in queryList:
	docList = indexFile.findDocumentsWithTerm(query)
	print query, docList