from objectClass import *
import bisect
import os
import struct
from math import log10

def computeScore(frequency, total, num):
	return (1+log10(frequency))*(log10(total/num))


class invertedIndex:

	def __init__(self):
		self.invertedList =  invertedObject()
		self.filename = "./invertedIndex.bin"
		self.configFile = "./inverted.config"
		self.tempFile = "./temp.bin"
		self.numBytes = 2
		self.sizeChar = 1
		self.sizeDoc = 2
		self.sizeFptr = 2
		self.distinctWords = 0
		self.totalDoc = 0
		self.memSize = 0
		self.offset = 0
		self.distinctWords = 0
		self.posSize = 2

		f = open(self.configFile, "r")
		content = f.read()

		lists = content.split("\n")
		self.memSize = int(lists[0])
		self.totalDoc = int(lists[1])
		self.distinctWords = int(lists[2])

		f.close()

	def readFromFile(self):
		f = open(self.filename, "rb")
		newObject = wordObject()

		f.seek(self.offset)

		currSize = 0
		numbytes = f.read(self.numBytes)

		if numbytes == "":
			f.close()
			return newObject

		numbytes = struct.unpack('<H', numbytes)
		numbytes = numbytes[0]

		while currSize < self.memSize:
			sizeword = ord(f.read(self.sizeChar))
			newObject.words.append(f.read(sizeword))
			newObject.fptr.append(struct.unpack('<H',f.read(self.sizeFptr))[0])

			numEntries = (numbytes - sizeword - self.sizeChar - self.sizeFptr)/(2*self.sizeDoc)

			doc = []
			freq = []

			for k in range(0, numEntries):
				doc.append(struct.unpack('<H',f.read(self.sizeDoc))[0])
				freq.append(struct.unpack('<H',f.read(self.sizeDoc))[0])

			newObject.frequency.append(freq)
			newObject.docs.append(doc)
			currSize += numbytes

			numbytes = f.read(self.numBytes)	
			if numbytes == "":
				break
			numbytes = struct.unpack('<H', numbytes)
			numbytes = numbytes[0]


		self.offset += currSize
		f.close()

		return newObject


	def writeToTemp(self, newObject):
		f = open(self.tempFile, "ab")

		for k in range(0, len(newObject.words)):
			numbytes = self.numBytes + self.sizeChar + len(newObject.words[k]) + self.sizeFptr + 2*(self.sizeDoc)*len(newObject.docs[k])
			f.write(struct.pack("H",numbytes))
			f.write(chr(len(newObject.words[k])))
			f.write(newObject.words[k])
			f.write(struct.pack("H",newObject.fptr[k]))

			for i in range(0, len(newObject.docs[k])):
				f.write(struct.pack("H",newObject.docs[k][i]))
				f.write(struct.pack("H",newObject.frequency[k][i]))

		f.close()


	def writeToobjectFile(self, fname, posList):
		filename = "./invertedFiles/word" + str(fname) + ".bin"
		out = open(filename, "wb") 
		format = "H"
		for k in range(0,len(posList)):
			data = struct.pack(format, posList[k])
			out.write(data)
		out.close()

	def appendToObjectFile(self, fname, posList):
		filename = "./invertedFiles/word" + str(fname) + ".bin"
		out = open(filename, "ab") 
		format = "H"

		for k in range(0,len(posList)):
			data = struct.pack(format, posList[k])
			out.write(data)

		out.close()

	def writeAdditionalToTemp(self, wordList, fname):
		f = open(self.tempFile, "ab")

		for k in range(0, len(wordList.words)):
			numbytes = self.numBytes + self.sizeChar + len(wordList.words[k]) + self.sizeFptr + 2*(self.sizeDoc)
			
			f.write(struct.pack("H",numbytes))
			f.write(chr(len(wordList.words[k])))
			f.write(wordList.words[k])
			f.write(struct.pack("H",self.distinctWords))
			f.write(struct.pack("H",fname))
			f.write(struct.pack("H",wordList.frequency[k]))

			self.writeToobjectFile(self.distinctWords, wordList.posList[k])
			self.distinctWords += 1

		f.close()

	def modifyConfigFile(self):
		f = open(self.configFile, "w")
		f.write(str(self.memSize) + "\n" + str(self.totalDoc+1) + "\n" + str(self.distinctWords))
		f.close()

	def modifyInvertedList(self,newList, fname):
		while True:
			newObject = self.readFromFile()

			if len(newObject.words) == 0:
				break

			for k in range(0, len(newObject.words)):

				# print newObject.words[k]
				# print newObject.docs[k]
				# print newObject.frequency[k]
				# print "\n"

				if newObject.words[k] in newList.words:
					index = newList.words.index(newObject.words[k])

					newObject.frequency[k].append(newList.frequency[index])
					newObject.docs[k].append(fname)
					self.appendToObjectFile(newObject.fptr[k], newList.posList[index])

					del newList.words[index]
					del newList.frequency[index]
					del newList.posList[index]

			self.writeToTemp(newObject)

		self.writeAdditionalToTemp(newList, fname)
		self.modifyConfigFile()

		os.remove(self.filename)
		os.rename(self.tempFile , self.filename)


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
		docList = []
		flag = False

		allDocList = []

		while True:
			newObject = self.readFromFile()

			if len(newObject.words) == 0:
				break

			for k in range(0,len(terms)):
				term = terms[k]
				if term in newObject.words:
					index = newObject.words.index(term)
					allDocList.append(newObject.docs[index])

		if len(allDocList) != len(terms):
			return []

		docList = allDocList[0]
		for k in range(0, len(allDocList)):
			docList = list(set(docList).intersection(allDocList[k]))
				
		return docList


	def findDocumentsWithPhrase(self, terms):

		termDict = {}
		while True:
			newObject = self.readFromFile()

			if len(newObject.words) == 0:
				break

			for k in range(0, len(terms)):
				term= terms[k]
				if term in newObject.words:
					newInfo = wordInfo()
					index = newObject.words.index(term)

					newInfo.docs = newObject.docs[index]
					newInfo.posList = self.findPosList(newObject.fptr[index], newObject.frequency[index])

					termDict[term] = newInfo


		return self.findSequentialTerms(termDict, terms)

	def findTopKDocuments(self, terms, numResult):
		termList = []
		docList = []
		freqList = []

		while True:
			newObject = self.readFromFile()

			if len(newObject.words) == 0:
				break


			for k in range(0, len(terms)):
				term = terms[k]
				if term in newObject.words:
					termList.append(term)
					index = newObject.words.index(term)
					docList.append(newObject.docs[index])
					freqList.append(newObject.frequency[index])

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
