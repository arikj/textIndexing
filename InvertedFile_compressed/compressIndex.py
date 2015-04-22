from objectClass import *
import bisect
import os
import struct
from huff import *


class convertTotxt:

	def __init__(self):
		self.filename = "./invertedIndex.bin"
		self.compressedFile = "./invertedIndexCompress.bin"
		self.newFile = "./invertedIndex.txt"
		self.configFile = "./inverted.config"
		self.numBytes = 2
		self.sizeChar = 1
		self.sizeDoc = 2
		self.sizeFptr = 2
		self.memSize = 0
		self.offset = 0
		self.posSize = 2
		self.huffTable = {}

		f = open(self.configFile, "r")
		content = f.read()

		lists = content.split("\n")
		self.memSize = int(lists[0])

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


	def convert(self):
		flag = False

		while True:
			newObject = self.readFromFile()

			if len(newObject.words) == 0:
				break

			f = open(self.newFile, "a")
			for k in range(0, len(newObject.words)):
				if flag == True:
					f.write("\n")
				flag = True
				f.write(newObject.words[k])
				f.write(" " + str(newObject.fptr[k]))

				for i in range(0, len(newObject.docs[k])):
					f.write(" " + str(newObject.docs[k][i]))
					f.write(" " + str(newObject.frequency[k][i]))
			f.close()


	def findHuffEncoding(self):
		self.huffTable = encodes(self.newFile)
		tablefile = open("./Hufftable.txt","w")

		flag = True
		for character in self.huffTable:
			if flag == True:
				tablefile.write(character.encode("utf-8") + "\t" + self.huffTable[character])
				flag = False
			else:
				tablefile.write("\n" + character.encode("utf-8") + "\t" + self.huffTable[character])
		tablefile.close()


	def createCompressedIndex(self):
		fil = open(self.compressedFile, "wb")
		with open(self.newFile, "r") as f:
			for line in f:
				if line == "":
					break

				encodedStr, pad = encodeString(line.strip(), self.huffTable)
				fil.write(struct.pack("H",len(encodedStr)))
				fil.write(struct.pack("H",pad))
				fil.write(encodedStr)
		fil.close()


classObject = convertTotxt()
classObject.convert()
classObject.findHuffEncoding()
classObject.createCompressedIndex()

