from math import log10
import time
import math
from preprocessing import *

queryFile = "../querySample.txt"
outputFile = "./output.txt"
outputDebug = True

numDocs = 1391
numSet = 2

preprocessClass = preprocessing()

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

g = open(outputFile, "w")

with open(queryFile, "r") as fil:
	for line in fil:
		index += 1
		lists = line.strip().split("\t")
		print "Processing query " + str(index)
		if lists[0] == '1':

			start = time.clock()
			docs = []
			queryterms = lists[1]
			queryterms = preprocessClass.processText(queryterms)
			queryList = queryterms.split( )

			for k in range(0,numDocs):
				filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
				f = open(filename,"r")
				content = f.read()
				content = preprocessClass.processText(content)
				f.close()

				flag = True
				for i in range(0,len(queryList)):
					if queryList[i] not in content:
						flag = False
						break
				if flag:
					docs.append(str(k))
			end  = time.clock()

			if end - start > 0:
				query1List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in docs)
				g.write(str1 + "\n\n")

		elif lists[0] == '2':
			start = time.clock()

			docs = []
			queryterms = lists[1]
			queryterms = preprocessClass.processText(queryterms)

			for k in range(0,numDocs):
				filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
				f = open(filename,"r")
				content = f.read()
				content = preprocessClass.processText(content)
				f.close()

				if queryterms in content:
					docs.append(str(k))
			end  = time.clock()

			if end - start > 0:
				query2List.append(end - start)
			if outputDebug:
				str1 = ' '.join(str(x) for x in docs)
				g.write(str1 + "\n\n")

		elif lists[0] == '3':
			start = time.clock()
			docs = []
			freq = []

			queryterms = lists[1]
			queryterms = preprocessClass.processText(queryterms)
			numResult = int(lists[2])

			queryList = queryterms.split( )
			for i in range(0,len(queryList)):
				docs.append([])
				freq.append([])

			for k in range(0,numDocs):
				filename = "../documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
				f = open(filename,"r")
				content = f.read()
				content = preprocessClass.processText(content)
				f.close()

				for i in range(0,len(queryList)):
					if queryList[i] in content:
						docs[i].append(str(k))
						freq[i].append(content.count(queryList[i]))

			# print queryList
			# print docs
			# print freq

			scoreDoc = {}
			for k in range(0, len(queryList)):
				size = len(docs[k])
				for i in range(0, size):
					if docs[k][i] not in scoreDoc:
						scoreDoc[docs[k][i]] = computeScore(freq[k][i], numDocs, size)

					else:
						scoreDoc[docs[k][i]] += computeScore(freq[k][i], numDocs, size)

			newList = sorted(scoreDoc.iteritems(), key=lambda x:-x[1])[:min(numResult, len(scoreDoc))]
			end  = time.clock()

			if end - start > 0:
				query3List.append(end - start)
			if outputDebug:
				for value in newList:
					g.write("Document: " + str(value[0]) + " score: " + str(value[1]) + "\n")
				g.write("\n")

		else:
			if outputDebug:
				g.write("Invalid option\n\n")


g.close()
allTimeResult(query1List, query2List, query3List)
