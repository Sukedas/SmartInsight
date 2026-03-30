import sqlite3

class Database:
    """Clase para manejar la integración con la base de datos existente (RF8)."""
    
    def __init__(self, db_path="DB/smartinsight.db"):
        self.db_path = db_path
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Error conectando a la base de datos: {e}")

    def execute_query(self, query, params=()):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        return None

    def fetch_all(self, query, params=()):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        return []
