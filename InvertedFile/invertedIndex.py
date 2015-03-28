class invertedIndex:

	def __init__(self):
		self.invertedList = {}
		self.filename = "./invertedIndex.txt"

	def readFromFile(self):
		contents = []
		with open(self.filename) as f:
			contents = [x.strip('\n') for x in f.readlines()]

		for content in contents:
			terms = content.split("\t")
			self.invertedList[terms[0]] = []

			for k in range(1, len(terms)):
				self.invertedList[terms[0]].append(terms[k])


	def writeBackToFile(self):
		f = open(self.filename, "w")

		for key, value in self.invertedList.iteritems():
			line = key

			for k in range(0,len(value)):
				line += "\t" + str(value[k])
			line += "\n"
			f.write(line)
		f.close()


	def modifyInvertedList(self,newList, index):
		for word in newList:
			if word not in self.invertedList:
				self.invertedList[word] = [index]
			else:
				self.invertedList[word].append(index)

	def findDocumentsWithTerm(self, term):
		if term not in self.invertedList:
			return []
		else:
			return self.invertedList[term]



