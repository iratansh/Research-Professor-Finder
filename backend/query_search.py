import sqlite3
from typing import List

class ProfessorSearch:
    def __init__(self, db_path: str = '../professorInfo.db'):
        self.db_path = db_path
        # Updated search columns: using only non-HTML fields from the new DB schema.
        self.search_columns = [
            'name', 'faculty', 'title', 'phone', 'location', 'text_overview'
        ]
        
    def search(self, keywords: List[str]):
        if not keywords:
            return []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query, params = self._build_query(keywords)
            cursor.execute(query, params)
            results = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description]

    def _build_query(self, keywords: List[str]):
        match_expressions = []
        params = []
        
        # Build the WHERE clause (6 columns * 2 keywords = 12 placeholders).
        for col in self.search_columns:
            column_conditions = " OR ".join([f"{col} LIKE ?" for _ in keywords])
            match_expressions.append(f"({column_conditions})")
            params.extend([f"%{kw}%" for kw in keywords])
        
        # Build the match count expression: for each column, check all keywords.
        match_count_expr = " + ".join(
            [
                " + ".join([f"CASE WHEN {col} LIKE ? THEN 1 ELSE 0 END" for _ in keywords])
                for col in self.search_columns
            ]
        )
        # For each column, add parameters for each keyword.
        params.extend([f"%{kw}%" for col in self.search_columns for kw in keywords])
        
        query = f"""
        SELECT *, ({match_count_expr}) AS match_count
        FROM professors
        WHERE {" OR ".join(match_expressions)}
        ORDER BY match_count DESC;
        """
        
        return query, params

    def set_search_columns(self, columns: List[str]):
        self.search_columns = columns
