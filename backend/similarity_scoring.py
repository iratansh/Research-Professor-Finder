from selection_query import ProfessorSearch
from quick_sort import QuickSort
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from sqlalchemy import create_engine, text


class ProfessorMatcher:
    def __init__(self, db_url: str, model_name: str = "all-MiniLM-L6-v2"):
        self.engine = create_engine(db_url)
        self.model = SentenceTransformer(model_name)
        self.professors: List[Dict] = []
        self.embeddings: np.ndarray = None
        self.professor_search = ProfessorSearch()

    def load_data(self):
        """Load professor data from SQL database"""
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                SELECT name, department, research_description 
                FROM professors
            """
                )
            )
            self.professors = [dict(row) for row in result]

            if not self.professors:
                raise ValueError("No professors found in database")

            # Precompute embeddings once
            descriptions = [p["research_description"] for p in self.professors]
            self.embeddings = self.model.encode(descriptions)

    def get_scores(self, query: str, top_k: int = 10) -> List[Dict]:
        """Return sorted list of professors with scores"""
        if not self.professors:
            raise RuntimeError("Call load_data() first")

        query_embed = self.model.encode([query])
        similarities = cosine_similarity(query_embed, self.embeddings)[0]

        scored_profs = []
        for idx, prof in enumerate(self.professors):
            scored_profs.append({**prof, "similarity_score": float(similarities[idx])})

        qSort = QuickSort(scored_profs)
        return qSort.sort(top_k)


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
