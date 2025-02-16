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
        return text.strip()