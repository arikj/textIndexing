from objectClass import *
import bisect
import os
import struct
from math import log10
from huff import *

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))


class invertedIndex:

	def __init__(self):
		self.invertedList =  invertedObject()
		self.filename = "./invertedIndexCompress.bin"
		self.configFile = "./inverted.config"
		self.numBytes = 2
		self.sizeChar = 1
		self.sizeDoc = 2
		self.sizeFptr = 2
		self.sizePad = 2
		self.distinctWords = 0
		self.totalDoc = 0
		self.memSize = 0
		self.offset = 0
		self.distinctWords = 0
		self.posSize = 2
		self.huffTable = {}

		f = open(self.configFile, "r")
		content = f.read()

		lists = content.split("\n")
		self.memSize = int(lists[0])
		self.totalDoc = int(lists[1])
		#self.distinctWords = int(lists[2])

		f.close()

		with open("Hufftable.txt", "r") as f:
			for line in f:
				lists = line.split('\t')
				self.huffTable[lists[0]] = lists[1].strip()

		self.decodeTree = createTree()
		self.decodeTree.recreateTree(self.huffTable)


	def readFromFile(self):
		f = open(self.filename, "rb")
		newObject = compressObject()

		f.seek(self.offset)

		currSize = 0
		numbytes = f.read(self.numBytes)


		if numbytes == "":
			f.close()
			return newObject

		numbytes = struct.unpack('<H', numbytes)
		numbytes = numbytes[0]


		while currSize < self.memSize:
			padding = struct.unpack('<H',f.read(self.sizePad))[0]
			readEntry = f.read(numbytes)

			newObject.compressString.append(readEntry)
			newObject.pad.append(padding)

			currSize += numbytes + self.sizePad + self.numBytes

			numbytes = f.read(self.numBytes)	
			if numbytes == "":
				break
			numbytes = struct.unpack('<H', numbytes)
			numbytes = numbytes[0]


		self.offset += currSize
		f.close()

		return newObject





	def findPosList(self, fname, frequency):
		filename = "./invertedFiles/word" + str(fname) + ".bin"
		f = open(filename, "rb")

		posList = []
		for freq in frequency:
			newList = []
			for k in range(0, freq):
				newList.append(struct.unpack('<H',f.read(self.sizeDoc))[0])
			posList.append(newList)
		f.close()

		return posList


	def extractData(self, encodedString, padding):
		newString = self.decodeTree.decodeHuff(encodedString, padding, self.huffTable)
		newObject = wordObjectClass()

		if newString == "":
			return newObject

		newList = newString.split(" ")

		newObject.word = newList[0]
		newObject.fptr = int(newList[1])

		for k in range(2,len(newList),2):
			newObject.docs.append(int(newList[k]))
			newObject.frequency.append(int(newList[k+1]))

		return newObject

	def findSequentialTerms(self, termDict, terms):
		docList = []
		posList = []
		flag = True

		for term in terms:

			if term not in termDict:
				return []

			if flag == True:
				docList = termDict[term].docs
				for k in range(0, len(docList)):
					posList.append(termDict[term].posList[k])
				flag = False

			else:
				removeElem = []
				for k in range(0,len(docList)):
					if docList[k] in termDict[term].docs:
						matchIndex = termDict[term].docs.index(docList[k])
						newVector = []
						for i in range(0, len(posList[k])):
							found = False
							for j in range(0, len(termDict[term].posList[matchIndex])):
								if posList[k][i] + 1 == termDict[term].posList[matchIndex][j]:
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

		return docList


	def findDocumentsWithTerm(self, terms):
		self.offset = 0
		docList = []
		flag = False

		allDocList = []

		while True:
			newObject = self.readFromFile()

			if len(newObject.pad) == 0:
				break

			for k in range(0, len(newObject.pad)):
				decodedData = self.extractData(newObject.compressString[k], newObject.pad[k])

				if decodedData.word in terms:
					allDocList.append(decodedData.docs)

		if len(allDocList) != len(terms):
			return []

		docList = allDocList[0]
		for k in range(0, len(allDocList)):
			docList = list(set(docList).intersection(allDocList[k]))
				
		return docList


	def findDocumentsWithPhrase(self, terms):
		self.offset = 0

		termDict = {}
		while True:
			newObject = self.readFromFile()

			if len(newObject.pad) == 0:
				break

			for k in range(0, len(newObject.pad)):
				decodedData = self.extractData(newObject.compressString[k], newObject.pad[k])

				if decodedData.word in terms:
					newInfo = wordInfo()

					newInfo.docs = decodedData.docs
					newInfo.posList = self.findPosList(decodedData.fptr, decodedData.frequency)

					termDict[decodedData.word] = newInfo

		return self.findSequentialTerms(termDict, terms)


	def findTopKDocuments(self, terms, numResult):
		self.offset = 0

		termList = []
		docList = []
		freqList = []

		while True:
			newObject = self.readFromFile()

			if len(newObject.pad) == 0:
				break

			for k in range(0, len(newObject.pad)):
				decodedData = self.extractData(newObject.compressString[k], newObject.pad[k])

				if decodedData.word in terms:
					termList.append(decodedData.word)
					docList.append(decodedData.docs)
					freqList.append(decodedData.frequency)

		scoreDoc = {}
		for k in range(0, len(termList)):
			size = len(docList[k])
			for i in range(0, size):
				if docList[k][i] not in scoreDoc:
					scoreDoc[docList[k][i]] = computeScore(freqList[k][i], self.totalDoc, size)

				else:
					scoreDoc[docList[k][i]] += computeScore(freqList[k][i], self.totalDoc, size)

		newList = sorted(scoreDoc.iteritems(), key=lambda x:-x[1])[:min(numResult, len(scoreDoc))]

		return newList
