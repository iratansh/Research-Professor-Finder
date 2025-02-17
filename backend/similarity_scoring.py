from quick_sort import QuickSort
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import re
from query_search import ProfessorSearch


class ProfessorMatcher:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.professors: List[Dict] = []
        self.embeddings: np.ndarray = None
        self.id_to_idx = {}
        self.professor_search = ProfessorSearch()

    def load_data(self):
        self.professors = self.professor_search.get_all_professors()
        self.id_to_idx = {prof["id"]: i for i, prof in enumerate(self.professors)}
        descriptions = [
            f"{prof['text_overview']} {prof['title']}" for prof in self.professors
        ]
        self.embeddings = self.model.encode(descriptions)

    def get_professors(self, keywords, top_k=10):
        if not self.professors:
            raise RuntimeError("Call load_data() first")

        relevant_profs = self.professor_search.search(keywords)
        if not relevant_profs:
            return []
        clean_query = self._clean_query(" ".join(keywords))
        query_embed = self.model.encode([clean_query])
        relevant_ids = [prof["id"] for prof in relevant_profs]
        relevant_indices = [self.id_to_idx[pid] for pid in relevant_ids]
        relevant_embeddings = self.embeddings[relevant_indices]
        similarities = cosine_similarity(query_embed, relevant_embeddings)[0]
        scored_tuples = [
            (relevant_profs[i]["id"], float(similarities[i]))
            for i in range(len(relevant_profs))
        ]
        qsort = QuickSort(scored_tuples)
        sorted_tuples = qsort.sort(top_k)
        return [self._get_prof_by_id(pid) for pid, _ in sorted_tuples]

    def _clean_query(self, text: str) -> str:
        text = text.lower()
        return re.sub(r"[^\w\s]", "", text).strip()

    def _get_prof_by_id(self, pid: int) -> Dict:
        return self.professors[self.id_to_idx[pid]]


if __name__ == "__main__":
    keywords = ["machine learning", "healthcare", "Jocelyn King"]
    matcher = ProfessorMatcher()
    matcher.load_data()
    print(matcher.get_professors(keywords))
