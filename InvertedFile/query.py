from invertedIndex import *
from preprocessing import *
import math
from math import log10
import time

queryFile = "../querySample.txt"
outputFile = "./output.txt"
outputDebug = True

def average(s): 
	if len(s) == 0:
		return 0.0

	return sum(s) * 1.0 / len(s)

def timeResult(timeupdate):
	mean = average(timeupdate)
	variance = map(lambda x: (x - mean)**2, timeupdate)
	stdev = math.sqrt(average(variance))
	return mean, stdev

def allTimeResult(time1, time2, time3):
	f = open("timeResult.txt","w")

	if len(time1) > 0:
		mean, stdev = timeResult(time1)
		f.write("---------- Term Queries-----------\n")
		f.write("Minimum: " + str(min(time1)) + "\n")
		f.write("Maximum: " + str(max(time1)) + "\n")
		f.write("Mean: " + str(mean) + "\n")
		f.write("Standard deviation: " + str(stdev) + "\n")

	if len(time2) > 0:
		mean, stdev = timeResult(time2)
		f.write("---------- Phrase Queries-----------\n")
		f.write("Minimum: " + str(min(time2)) + "\n")
		f.write("Maximum: " + str(max(time2)) + "\n")
		f.write("Mean: " + str(mean) + "\n")
		f.write("Standard deviation: " + str(stdev) + "\n")

	if len(time3) > 0:
		mean, stdev = timeResult(time3)
		f.write("---------- Ranking Queries-----------\n")
		f.write("Minimum: " + str(min(time3)) + "\n")
		f.write("Maximum: " + str(max(time3)) + "\n")
		f.write("Mean: " + str(mean) + "\n")
		f.write("Standard deviation: " + str(stdev) + "\n")


	f.close() 

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))

# print "1. Search by terms query\n2. Search by phrase query\n3. Ranking of documents based on query"
# option = int(raw_input("Select an option: "))

index = 0

query1List = []
query2List = []
query3List = []

f = open(outputFile, "w")

with open(queryFile, "r") as fil:
	for line in fil:
		index += 1
		lists = line.strip().split("\t")
		print "Processing query " + str(index)
		if lists[0] == '1':

			start = time.clock()

			preprocessText = preprocessing()
			indexFile = invertedIndex()

			queryterms = lists[1]
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
					
			end  = time.clock()

			if end - start > 0:
				query1List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in docList)
				f.write(str1 + "\n\n")

		elif lists[0] == '2':
			start = time.clock()

			preprocessText = preprocessing()
			indexFile = invertedIndex()

			queryterms = lists[1]
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

			end  = time.clock()

			if end - start > 0:
				query2List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in docList)
				f.write(str1 + "\n\n")

		elif lists[0] == '3':
			start = time.clock()
			preprocessText = preprocessing()
			indexFile = invertedIndex()

			queryterms = lists[1]
			topResult = int(lists[2])
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
			end  = time.clock()

			if end - start > 0:
				query3List.append(end - start)
				
			if outputDebug:
				for value in newList:
					f.write("Document: " + str(value[0]) + " score: " + str(value[1]) + "\n")
				f.write("\n")

		else:
			if outputDebug:
				f.write("Invalid option\n\n")


f.close()
allTimeResult(query1List, query2List, query3List)

