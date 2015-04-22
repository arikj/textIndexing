import nltk
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
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
		result = ""

		for word in wordSet:
			word = word.lower()
			word = self.lemmatizer.lemmatize(word)
			word = self.stemmer.stem(word);
			
			if word in stop:
				continue
			if not re.match(self.pattern,word):
				continue
			result += word + " "

		return result


