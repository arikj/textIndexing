from objectClass import *

class invertedIndex:

	def __init__(self):
		self.invertedList =  invertedObject()
		self.filename = "./invertedIndex.txt"

	def readFromFile(self):
		contents = ""
		with open(self.filename) as f:
			contents = f.read()

		contentList = contents.split("\t")

		index = 0
		while index < len(contentList)-1:
			self.invertedList.words.append(contentList[index])
			index += 1
			freq = int(contentList[index])
			index += 1
			self.invertedList.frequency.append(freq)
			newObject = perWordObject()
			while freq > 0:
				newObject.document.append(int(contentList[index]))
				index +=1
				newFreq = int(contentList[index])
				index += 1
				freq -= newFreq
				newObject.frequency.append(newFreq)
				newVector = []
				for k in range(0, newFreq):
					newVector.append(int(contentList[index]))
					index += 1
				newObject.posList.append(newVector)
			self.invertedList.perWord.append(newObject)


	def printVal(self):
		for k in range(0, len(self.invertedList.words)):
			print self.invertedList.words[k] + "\t" + str(self.invertedList.frequency[k]) + "\t"

			
			for j in range(0, len(self.invertedList.perWord[k].document)):
				print str(self.invertedList.perWord[k].document[j]) + "\t" + str(self.invertedList.perWord[k].frequency[j]) + "\t"
				for i in range(0, self.invertedList.perWord[k].frequency[j]):
					print str(self.invertedList.perWord[k].posList[j][i]) + "\t"
			

	def writeBackToFile(self):
		f = open(self.filename, "w")

		for k in range(0, len(self.invertedList.words)):
			f.write(self.invertedList.words[k] + "\t" + str(self.invertedList.frequency[k]) + "\t") 

			for j in range(0, len(self.invertedList.perWord[k].document)):
				f.write(str(self.invertedList.perWord[k].document[j]) + "\t" + str(self.invertedList.perWord[k].frequency[j]) + "\t")
				for i in range(0, self.invertedList.perWord[k].frequency[j]):
					f.write(str(self.invertedList.perWord[k].posList[j][i]) + "\t")
		f.close()


	def modifyInvertedList(self,newList, index):
		for k in range(0, len(newList.words)):
			if newList.words[k] not in self.invertedList.words:
				self.invertedList.words.append(newList.words[k])
				self.invertedList.frequency.append(newList.frequency[k])
				newObject = perWordObject()
				newObject.document.append(index)
				newObject.frequency.append(newList.frequency[k])
				newObject.posList.append(newList.posList[k])
				self.invertedList.perWord.append(newObject)

			else:
				matchIndex = self.invertedList.words.index(newList.words[k])
				self.invertedList.frequency[matchIndex] += newList.frequency[k]
				self.invertedList.perWord[matchIndex].document.append(index)
				self.invertedList.perWord[matchIndex].frequency.append(newList.frequency[k])
				self.invertedList.perWord[matchIndex].posList.append(newList.posList[k])

'''
	def findDocumentsWithTerm(self, term):
		if term not in self.invertedList:
			return []
		else:
			return self.invertedList[term]
'''


