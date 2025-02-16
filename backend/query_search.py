import sqlite3
from typing import List, Dict

class ProfessorSearch:
    def __init__(self, db_path='./professorInfo.db'):
        self.db_path = db_path
        self.search_columns = [
            'name', 'faculty', 'title', 
            'phone', 'location', 'text_overview'
        ]

    def get_all_professors(self) -> List[Dict]:
        """Get complete professor list"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors")
            return [dict(row) for row in cursor.fetchall()]

    def search(self, keywords: List[str]) -> List[Dict]:
        """Find professors matching ANY keyword (original implementation)"""
        if not keywords:
            return []

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query, params = self._build_query(keywords)
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {str(e)}") from e

    def _build_query(self, keywords: List[str]):
        # Original implementation preserved
        match_expressions = []
        params = []
        
        for col in self.search_columns:
            column_conditions = " OR ".join([f"{col} LIKE ?" for _ in keywords])
            match_expressions.append(f"({column_conditions})")
            params.extend([f"%{kw}%" for kw in keywords])
        
        match_count_expr = " + ".join(
            [
                " + ".join([f"CASE WHEN {col} LIKE ? THEN 1 ELSE 0 END" for _ in keywords])
                for col in self.search_columns
            ]
        )
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