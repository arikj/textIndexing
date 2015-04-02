from objectClass import *
import bisect

class invertedIndex:

	def __init__(self):
		self.invertedList =  invertedObject()
		self.filename = "./invertedIndex.txt"
		self.distinctWords = 0

	def readFromFile(self):
		contents = ""
		with open(self.filename) as f:
			contents = f.read()

		contentList = contents.split("\n")
		for content in contentList:
			if content == "":
				break
			term, filename = content.split("\t")
			self.invertedList.words.append(term)
			self.invertedList.filename.append(filename)
			self.distinctWords += 1
			

	def writeBackToFile(self):
		f = open(self.filename, "w")

		for k in range(0, len(self.invertedList.words)):
			f.write(self.invertedList.words[k] + "\t" + str(self.invertedList.filename[k]) + "\n") 

		f.close()


	def modifyInvertedList(self,newList, index):

		for k in range(0, len(newList.words)):
			if newList.words[k] not in self.invertedList.words:
				insertIndex = (bisect.bisect_left(self.invertedList.words, newList.words[k]))
				self.invertedList.words.insert(insertIndex, newList.words[k])
				self.distinctWords += 1
				self.invertedList.filename.insert(insertIndex, self.distinctWords)
				
				newObject = perWordObject()
				newObject.totalFrequency = newList.frequency[k]
				newObject.document.append(index)
				newObject.frequency.append(newList.frequency[k])
				newObject.posList.append(newList.posList[k])
				newObject.writeToFile(self.distinctWords)

			else:
				matchIndex = self.invertedList.words.index(newList.words[k])
				objectFile = self.invertedList.filename[matchIndex]

				oldObject = perWordObject()
				oldObject.readFromFile(objectFile)

				newObject = perWordObject()
				newObject.document.append(index)
				newObject.totalFrequency = newList.frequency[k]
				newObject.frequency.append(newList.frequency[k])
				newObject.posList.append(newList.posList[k])

				oldObject.mergeObjects(newObject)
				oldObject.writeToFile(objectFile)




	def findDocumentsWithTerm(self, term):
		if term not in self.invertedList.words:
			return perWordObject()
		else:
			matchIndex = self.invertedList.words.index(term)
			objectFile = self.invertedList.filename[matchIndex]

			oldObject = perWordObject()
			oldObject.readFromFile(objectFile)

			return oldObject



