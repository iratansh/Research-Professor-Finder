import sqlite3
from typing import Optional, Dict, Any

class ProfessorQuery:
    def __init__(self, db_path: str = './professorInfo.db'):
        self.db_path = db_path

    def get_professor_by_id(self, professor_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a professor record by its ID.
        
        :param professor_id: The ID of the professor to retrieve.
        :return: A dictionary of the professor record if found, otherwise None.
        """
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

# Example usage:
if __name__ == '__main__':
    db = ProfessorQuery()  # You can pass a custom path if needed.
    professor_id = 1  # Replace with the desired professor ID.
    professor = db.get_professor_by_id(professor_id)
    
    if professor:
        print("Professor record found:")
        print(professor)
    else:
        print("No professor found with that ID.")
