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

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query, params = self._build_query(keywords)
                cursor.execute(query, params)
                results = cursor.fetchall()

                column_names = [desc[0] for desc in cursor.description]
                return [dict(zip(column_names, row)) for row in results]

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {str(e)}") from e

    def _build_query(self, keywords: List[str]):``
        match_expressions = []
        params = []
        
        # Build the WHERE clause to match any keyword in any search column.
        for col in self.search_columns:
            # For each column, create a condition for each keyword.
            column_conditions = " OR ".join([f"{col} LIKE ?" for _ in keywords])
            match_expressions.append(f"({column_conditions})")
            params.extend([f"%{kw}%" for kw in keywords])
        
        # Build the match count expression to rank results.
        match_count_expr = " + ".join(
            [f"CASE WHEN {col} LIKE ? THEN 1 ELSE 0 END" for col in self.search_columns]
        )
        params.extend([f"%{kw}%" for kw in keywords])
        
        query = f"""
        SELECT *, ({match_count_expr}) AS match_count
        FROM professors
        WHERE {" OR ".join(match_expressions)}
        ORDER BY match_count DESC;
        """
        
        return query, params

    def set_search_columns(self, columns: List[str]):
        self.search_columns = columns
