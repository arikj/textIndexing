from math import log10

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))



numDocs = 500
numSet = 2

print "1. Search by terms query\n2. Search by phrase query\n3. Ranking of documents based on query"
option = int(raw_input("Select an option: "))

if option == 1:
	docs = []
	queryterms = str(raw_input("Query terms: "))
	queryList = queryterms.split( )

	for k in range(0,numDocs):
		filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
		f = open(filename,"r")
		content = f.read()
		f.close()

		flag = True
		for i in range(0,len(queryList)):
			if queryList[i] not in content:
				flag = False
				break
		if flag:
			docs.append("doc"+str(k))
	print docs

elif option == 2:
	docs = []
	queryterms = str(raw_input("Query terms: "))

	for k in range(0,numDocs):
		filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
		f = open(filename,"r")
		content = f.read()
		f.close()

		if queryterms in content:
			docs.append("doc"+str(k))

	print docs


elif option == 3:
	docs = []
	freq = []

	queryterms = str(raw_input("Query terms: "))
	queryList = queryterms.split( )
	for i in range(0,len(queryList)):
		docs.append([])
		freq.append([])

	for k in range(0,numDocs):
		filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
		f = open(filename,"r")
		content = f.read()
		f.close()

		for i in range(0,len(queryList)):
			if queryList[i] in content:
				docs[i].append("doc"+str(k))
				freq[i].append(content.count(queryList[i]))

	# print queryList
	# print docs
	# print freq

	scoreDoc = {}
	numResult = 10
	for k in range(0, len(queryList)):
		size = len(docs[k])
		for i in range(0, size):
			if docs[k][i] not in scoreDoc:
				scoreDoc[docs[k][i]] = computeScore(freq[k][i], numDocs, size)

			else:
				scoreDoc[docs[k][i]] += computeScore(freq[k][i], numDocs, size)

	newList = sorted(scoreDoc.iteritems(), key=lambda x:-x[1])[:min(numResult, len(scoreDoc))]
	print newList

else:
	print "No such option"
