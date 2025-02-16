from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

class Preprocessor:
    def __init__(self):
        self.stopwords = stopwords.words('english')
        self.PorterStemmer = PorterStemmer()

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = text.split()
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [self.PorterStemmer.stem(word) for word in tokens]
        return ' '.join(tokens)
