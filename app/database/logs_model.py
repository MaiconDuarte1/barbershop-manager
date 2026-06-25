from app.database.database import get_connection


class LogsModel:

    @staticmethod
    def create_table():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def add(username, action):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO logs (
                username,
                action
            )
            VALUES (?, ?)
        """, (
            username,
            action
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM logs
            ORDER BY id DESC
        """)

        logs = cursor.fetchall()

        conn.close()

        return logs