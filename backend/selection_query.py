import sqlite3
from typing import List

class ProfessorSearch:
    def __init__(self, db_path: str = 'professorInfo.db'):
        self.db_path = db_path
        self.search_columns = [
            'name', 'faculty', 'header', 
            'contact', 'overview', 'links', 'courses'
        ]
        
    def search(self, keywords: List[str]):
        if not keywords:
            return []

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query, params = self._build_query(keywords)
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {str(e)}") from e

    def _build_query(self, keywords: List[str]):
        match_expressions = []
        params = []
        
        for kw in keywords:
            pattern = f"%{kw}%"
            for col in self.search_columns:
                match_expressions.append(f"(CASE WHEN {col} LIKE ? THEN 1 ELSE 0 END)")
                params.append(pattern)

        match_count_expr = " + ".join(match_expressions)
        
        query = f"""
        SELECT *, ({match_count_expr}) AS match_count
        FROM professors
        WHERE match_count > 0
        ORDER BY match_count DESC;
        """
        
        return query, params

    def set_search_columns(self, columns):
        self.search_columns = columns
