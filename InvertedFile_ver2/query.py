from invertedIndex import *
from preprocessing import *
from math import log10
import math
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

indexFile = invertedIndex()
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

			indexFile = invertedIndex()

			preprocessText = preprocessing()

			queryterms = lists[1]
			queryList = preprocessText.processText(queryterms)

			docList = []
			flag = True
			if len(queryList.words) > 0:				
				docList = indexFile.findDocumentsWithTerm(queryList.words)
			end  = time.clock()

			if end - start > 0:
				query1List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in docList)
				f.write(str1 + "\n\n")

		elif lists[0] == '2':
			start = time.clock()

			indexFile = invertedIndex()
			preprocessText = preprocessing()

			queryterms = lists[1]
			queryList = preprocessText.processText(queryterms)

			if len(queryList.words) > 0:
				docList = indexFile.findDocumentsWithPhrase(queryList.words)
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

		
			if len(queryList.words) > 0:
				newList = indexFile.findTopKDocuments(queryList.words, topResult)
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














