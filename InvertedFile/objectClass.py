import struct

class documentObject:

	def __init__(self):
		self.words = []
		self.frequency = []
		self.posList = []



class perWordObject:
	def __init__(self):
		self.totalFrequency =  0
		self.document = []
		self.frequency = []
		self.posList = []

		self.filePath = "./invertedFiles/word"
		self.byteSize = 2

	def readFromFile(self, filename):
		filename = self.filePath + str(filename) + ".bin"
		formats = "H"

		with open(filename, "rb") as f:
			byte = struct.unpack(formats, f.read(self.byteSize))[0]
			self.totalFrequency = int(byte)
			counter = self.totalFrequency
			
			while counter > 0:
				byte = struct.unpack(formats, f.read(self.byteSize))[0]
				self.document.append(int(byte))
				byte = struct.unpack(formats, f.read(self.byteSize))[0]
				self.frequency.append(int(byte))
				counter -= int(byte)
				size = int(byte)
				posVector = []
				for k in range(0,size):
					byte = struct.unpack(formats, f.read(self.byteSize))[0]
					posVector.append(int(byte))
				self.posList.append(posVector)


	def writeToFile(self, filename):
		filename = self.filePath + str(filename) + ".bin"
		out = open(filename, "wb") 
		formats = "H"

		data = struct.pack(formats, self.totalFrequency)
		out.write(data)

		for k in range(0,len(self.document)):
			data = struct.pack(formats, self.document[k])
			out.write(data)

			data = struct.pack(formats, self.frequency[k])
			out.write(data)

			for i in range(0, self.frequency[k]):
				data = struct.pack(formats, self.posList[k][i])
				out.write(data)

		out.close()

	def mergeObjects(self, newObject):
		self.totalFrequency += newObject.totalFrequency

		for k in range(0, len(newObject.document)):
			self.document.append(newObject.document[k])
			self.frequency.append(newObject.frequency[k])
			self.posList.append(newObject.posList[k])
			

class invertedObject:

	def __init__(self):
		self.words = []
		self.filename = []