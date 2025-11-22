from models.database import Database

class BaseModel:
    table_name = None

    def __init__(self):
        self.db = Database()

    def query(self, sql, params=None, fetchone=False):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, params)
        result = cursor.fetchone() if fetchone else cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return result
