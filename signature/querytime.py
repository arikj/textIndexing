from preprocessing import *
import math
from math import log10
import time

queryFile = "../querySample.txt"
outputFile = "./output.txt"
outputDebug = True

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))

numDoc = 1390
direc = "2"
cache = {}
tablefile = "table.txt"
def readTable():
	fpr = open(tablefile,"r")
	line = fpr.read()
	# print line
	count = 0
	for row in line.split("\n"):
		key,value = row.split("\t")
		# print key + " "+value
		cache[key]  = value
		count+=1
		# print count
	# print cache
def convertToBinary(ascii):
    bitstring = ''
    bitstring = '{0:08b}'.format(ascii)
    #print bitstring
    return bitstring
def decode(query):
	bitstring = ''
	for character in query:
		if character in cache:
			bitstring += cache[character]
			continue
		print "encoding not found"
		bitstring += '1'
	return bitstring

def read(x):
	filer = "write/set"+direc+"/write"+str(x)+".bin"
	fpr = open(filer,"rb")
	buff = fpr.read(1)
	bitstring = ''
	while buff!='':
		ascii = ord(buff)
		bitstring += convertToBinary(ascii)
		buff = fpr.read(1)
	fpr.close()
	return bitstring
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


# print "1. Search by terms query\n2. Search by phrase query\n3. Ranking of documents based on query"
# option = int(raw_input("Select an option: "))



query1List = []
query2List = []
query3List = []
index = 0
f = open(outputFile, "w")
readTable()
with open(queryFile, "r") as fil:
	preProcess = preprocessing()
	for line in fil:
		index += 1
		print "processing query: " + str(index)
		lists = line.strip().split("\t")
		query = lists[1]
		query = preProcess.processText(query)
		# print query
		# print lists
		if lists[0] == '1':

			start = time.clock()
			termList = []
			resultList = []
			huffList = []
			termList = query.strip().split(" ")
			# print termList
			for terms in termList:
				# print "in"
				huffList.append(decode(terms))
			# print huffList
			for x in range(0,numDoc):
				flag = True
				bitstring = read(x)
				for i in range(0,len(huffList)):
					if huffList[i] not in bitstring:
						flag = False
						break
				if flag:
					resultList.append(x)
			end  = time.clock()

			if end - start > 0:
				query1List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in resultList)
				f.write(str1 + "\n\n")

		elif lists[0] == '2':
			start = time.clock()
			resultList = []
			querycode = decode(query)
			for x in range(0,numDoc):
			 	bitstring = read(x)
				if querycode in bitstring:
					# print "found word " + query + " in doc "+ str(x)
					resultList.append(x)
					continue 
				# print "not found word " + query + " in doc "+ str(x)
			end  = time.clock()

			if end - start > 0:
				query2List.append(end - start)

			if outputDebug:
				str1 = ' '.join(str(x) for x in resultList)
				f.write(str1 + "\n\n")

		elif lists[0] == '3':
			huffList = []
			start = time.clock()
			termList = []
			numResult = int(lists[2])
			# print "query: "+query
			termList = query.strip().split(" ")
			docList = []
			freqList = []
			for terms in termList:
				huffList.append(decode(terms))
				docList.append([])
				freqList.append([])
			# print termList
			# print huffList
			# print len(termList)
			# print len(huffList)
			for x in range(0,numDoc):
				bitstring = read(x)
				for i in range(0,len(huffList)):
					count = bitstring.count(huffList[i])
					# print count
					if count > 0:
						docList[i].append(x)
						freqList[i].append(count)
						continue
			# print docList
			# print freqList
			scoreDoc = {}
			for k in range(0, len(termList)):
				size = len(docList[k])
				for i in range(0, size):
					if docList[k][i] not in scoreDoc:
						scoreDoc[docList[k][i]] = computeScore(freqList[k][i], numDoc, size)

					else:
						scoreDoc[docList[k][i]] += computeScore(freqList[k][i], numDoc, size)

			newList = sorted(scoreDoc.iteritems(), key=lambda x:-x[1])[:min(numResult, len(scoreDoc))]
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
