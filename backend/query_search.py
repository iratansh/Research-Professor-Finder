import sqlite3
from typing import List, Dict, Any
import sys


class ProfessorSearch:
    def __init__(
        self, db_path="./professorInfo.db", column_weights: Dict[str, int] = None
    ):
        self.db_path = db_path
        self.search_columns = [
            "name",
            "faculty",
            "title",
            "phone",
            "location",
            "text_overview",
        ]
        if column_weights is None:
            self.column_weights = {
                "name": 3,
                "faculty": 2,
                "title": 2,
                "phone": 1,
                "location": 1,
                "text_overview": 1,
            }
        else:
            self.column_weights = column_weights

    def set_column_weights(self, column_weights: Dict[str, int]):
        """Allows setting custom weights for the search columns."""
        self.column_weights = column_weights

    def get_all_professors(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors")
            return [dict(row) for row in cursor.fetchall()]

    def search(self, keywords: List[Any]) -> List[Dict]:
        if not keywords:
            return []

        keywords = [str(kw) for kw in keywords]

        flattened_keywords = []
        for keyword in keywords:
            flattened_keywords.extend(keyword.split())
        keywords = flattened_keywords

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
        match_count_exprs = []
        match_params = []
        for col in self.search_columns:
            weight = self.column_weights.get(col, 1)
            for kw in keywords:
                match_count_exprs.append(
                    f"CASE WHEN {col} LIKE ? COLLATE NOCASE THEN {weight} ELSE 0 END"
                )
                match_params.append(f"%{kw}%")

        # Build expressions and parameters for the WHERE clause
        where_expressions = []
        where_params = []
        for col in self.search_columns:
            conditions = " OR ".join([f"{col} LIKE ? COLLATE NOCASE" for _ in keywords])
            where_expressions.append(f"({conditions})")
            where_params.extend([f"%{kw}%" for kw in keywords])

        # Combine parameters: match_count parameters come first because their placeholders
        # appear before those in the WHERE clause in the query.
        params = match_params + where_params

        # Join all match expressions with a plus sign to sum up the scores
        match_count_expr = " + ".join(match_count_exprs)

        query = f"""
        SELECT *, ({match_count_expr}) AS match_count
        FROM professors
        WHERE {" OR ".join(where_expressions)}
        ORDER BY match_count DESC;
        """
        return query, params


if __name__ == "__main__":
    search = ProfessorSearch()
    # Accept multiple keywords from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python query_search.py <keyword> [additional keywords...]")
        sys.exit(1)

    # Pass sys.argv[1:] to ensure a list of keywords is used.
    results = search.search(sys.argv[1:])
    for professor in results[:10]:
        print(professor["name"])
