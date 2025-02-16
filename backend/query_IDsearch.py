import sqlite3
from typing import Optional, Dict, Any

class ProfessorQuery:
    def __init__(self, db_path: str = './professorInfo.db'):
        self.db_path = db_path

    def get_professor_by_id(self, professor_id: int) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM professors WHERE id = ?"
            cursor.execute(query, (professor_id,))
            row = cursor.fetchone()
            if row is None:
                return None  # No row found for the given ID

            # Retrieve column names from the cursor description.
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))