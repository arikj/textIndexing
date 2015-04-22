from objectClass import *
import bisect
import os
import struct

class invertedIndex:

	def __init__(self):
		self.invertedList =  invertedObject()
		self.filename = "./invertedIndex.bin"
		self.configFile = "./inverted.config"
		self.tempFile = "./temp.bin"
		self.numBytes = 4
		self.sizeChar = 1
		self.sizeDoc = 4
		self.sizeFptr = 0
		self.distinctWords = 0
		self.totalDoc = 0
		self.memSize = 0;
		self.offset = 0;

		f = open(self.configFile, "r")
		self.memSize = int(f.read())
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

		numbytes = struct.unpack('<I', numbytes)
		numbytes = numbytes[0]

		while currSize < self.memSize:
			sizeword = ord(f.read(self.sizeChar))
			newObject.words.append(f.read(sizeword))
			#newObject.fptr.append(int(f.read(self.sizeFptr)))

			numEntries = (numbytes - sizeword - self.sizeChar)/(2*self.sizeDoc)

			doc = []
			freq = []

			for k in range(0, numEntries):
				doc.append(struct.unpack('<I',f.read(self.sizeDoc))[0])
				freq.append(struct.unpack('<I',f.read(self.sizeDoc))[0])

			newObject.frequency.append(freq)
			newObject.docs.append(doc)
			currSize += numbytes

			numbytes = f.read(self.numBytes)	
			if numbytes == "":
				break
			numbytes = struct.unpack('<I', numbytes)
			numbytes = numbytes[0]


		self.offset += currSize
		f.close()

		return newObject


	def writeToTemp(self, newObject):
		f = open(self.tempFile, "ab")

		for k in range(0, len(newObject.words)):
			numbytes = self.numBytes + self.sizeChar + len(newObject.words[k]) + self.sizeFptr + 2*(self.sizeDoc)*len(newObject.docs[k])
			f.write(struct.pack("i",numbytes))
			f.write(chr(len(newObject.words[k])))
			f.write(newObject.words[k])
			# f.write(newObject.fptr[k])

			for i in range(0, len(newObject.docs[k])):
				f.write(struct.pack("i",newObject.docs[k][i]))
				f.write(struct.pack("i",newObject.frequency[k][i]))

		f.close()


	def writeAdditionalToTemp(self, wordList, fname):
		f = open(self.tempFile, "ab")

		for k in range(0, len(wordList.words)):
			numbytes = self.numBytes + self.sizeChar + len(wordList.words[k]) + self.sizeFptr + 2*(self.sizeDoc)
			
			f.write(struct.pack("i",numbytes))
			f.write(chr(len(wordList.words[k])))
			f.write(wordList.words[k])
			# f.write(fptr)
			f.write(struct.pack("i",fname))
			f.write(struct.pack("i",wordList.frequency[k]))

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

					del newList.words[index]
					del newList.frequency[index]
					del newList.posList[index]

			self.writeToTemp(newObject)

		self.writeAdditionalToTemp(newList, fname)
		os.remove(self.filename)
		os.rename(self.tempFile , self.filename)


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





