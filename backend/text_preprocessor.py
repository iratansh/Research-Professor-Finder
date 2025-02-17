from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from autocorrect import Speller
import re

class Preprocessor:
    def __init__(self):
        self.stopwords = stopwords.words('english')
        self.stemmer = PorterStemmer()
        self.spell = Speller()
        self.ml_terms = {
            'lstm', 'bert', 'nlp', 'relu', 'mnist', 'keras',
            'tensorflow', 'pytorch', 'sklearn', 'numpy', 'pandas',
            'matplotlib', 'scipy', 'seaborn', 'conda', 'jupyter',
            'kaggle', 'colab', 'cuda', 'gpu', 'cpu', 'api'
        }

    def preprocess(self, text, autocorrect=True, remove_stopwords=False, stem=False):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()
        
        if autocorrect:
            corrected_words = []
            for word in words:
                if word in self.ml_terms:
                    corrected_words.append(word)
                else:
                    corrected_words.append(self.spell(word))
            words = corrected_words
        
        if remove_stopwords:
            words = [word for word in words if word not in self.stopwords]
        if stem:
            words = [self.stemmer.stem(word) for word in words]
            
        return ' '.join(words).strip()

    def add_domain_terms(self, terms):
        self.ml_terms.update(set(terms))