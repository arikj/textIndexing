import nltk
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer


class preprocessing:

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.stemmer = PorterStemmer()
		self.tokenizer = RegexpTokenizer(r'\w+')

	def processText(self, text):
		wordList = self.tokenizer.tokenize(text)
		filteredWords = [w for w in wordList if not w in stopwords.words('english')]
		allWordList = []

		for word in filteredWords:
			word = word.lower()
			word = self.lemmatizer.lemmatize(word)
			word = self.stemmer.stem(word);

			if word not in allWordList:
				allWordList.append(word)

		return allWordList


