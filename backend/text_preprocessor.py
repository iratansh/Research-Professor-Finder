import nltk
import string
import re

class Preprocessor:
    def __init__(self):
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.punctuations = string.punctuation
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stopwords and token not in self.punctuations]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(tokens)
