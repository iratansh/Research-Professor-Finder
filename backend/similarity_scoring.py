from query_search import ProfessorSearch
from quick_sort import QuickSort
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict


class ProfessorMatcher:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.professors: List[Dict] = []
        self.embeddings: np.ndarray = None
        self.professor_search = ProfessorSearch()

    def get_professors(self, keywords, top_k: int = 10) -> List[Dict]:
        """Return sorted list of professors with scores"""        
        relevant_profs = self.professor_search.search(keywords)
        print(relevant_profs)
        query_embed = self.model.encode(relevant_profs)
        similarities = cosine_similarity(query_embed, self.embeddings)[0]

        scored_profs = []
        for idx, prof in enumerate(self.professors):
            scored_profs.append({**prof, "similarity_score": float(similarities[idx])})

        qSort = QuickSort(scored_profs)
        return qSort.sort(top_k)

if __name__ == "__main__":
    keywords = ["machine learning", "healthcare", "Jocelyn King"]
    matcher = ProfessorMatcher()
    print(matcher.get_professors(keywords))

"""
THIS IS HOW TO USE 
# Your teammates will use it like this in their FastAPI code
matcher = ProfessorMatcher(db_url="postgresql://user:pass@localhost/dbname")
matcher.load_data()

# For each API request
results = matcher.get_scores("machine learning healthcare")
"""

"""
Output structure:
[
    {
        "name": "Dr. Alice Chen",
        "department": "Computer Science",
        "research_description": "...",
        "similarity_score": 0.92
    },
    {
        "name": "Dr. Maria Lopez",
        "department": "Engineering", 
        "research_description": "...",
        "similarity_score": 0.85
    }
]
"""
