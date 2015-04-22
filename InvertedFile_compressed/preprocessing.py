import nltk
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from objectClass import *
import re

class preprocessing:

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.stemmer = PorterStemmer()
		self.tokenizer = RegexpTokenizer(r'\w+')
		self.pattern = r'[a-z0-9]+'

	def processText(self, text):
		text = text.decode("utf8")
		wordSet = self.tokenizer.tokenize(text)
		stop = stopwords.words('english')
		wordList = documentObject()
		index = 0
		distinct = 0
		
		for word in wordSet:
			word = word.lower()
			word = self.lemmatizer.lemmatize(word)
			word = self.stemmer.stem(word);
			
			if word in stop:
				continue

			if not re.match(self.pattern,word):
				continue

			if word not in wordList.words:
				wordList.words.append(word)
				wordList.frequency.append(1)
				wordList.posList.append([index])
			else:
				matchIndex = wordList.words.index(word)
				wordList.frequency[matchIndex] += 1
				wordList.posList[matchIndex].append(index)

			index += 1

		return wordList


