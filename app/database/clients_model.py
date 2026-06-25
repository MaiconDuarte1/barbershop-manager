from app.database.database import get_connection


class ClientsModel:

    @staticmethod
    def create_table():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                observations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM clients
            ORDER BY name
        """)

        clients = cursor.fetchall()

        conn.close()

        return clients

    @staticmethod
    def create(name, phone, observations):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clients (
                name,
                phone,
                observations
            )
            VALUES (?, ?, ?)
        """, (
            name,
            phone,
            observations
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(client_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM clients WHERE id = ?",
            (client_id,)
        )

        conn.commit()
        conn.close()


    @staticmethod
    def update(client_id, name, phone, observations):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clients
            SET
                name = ?,
                phone = ?,
                observations = ?
            WHERE id = ?
        """, (
            name,
            phone,
            observations,
            client_id
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def get_by_id(client_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM clients WHERE id = ?",
            (client_id,)
        )

        client = cursor.fetchone()

        conn.close()

        return client
    


    @staticmethod
    def search(text):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM clients
            WHERE name LIKE ?
            ORDER BY name
        """, (
            f"%{text}%",
        ))

        clients = cursor.fetchall()

        conn.close()

        return clients
    

    @staticmethod
    def get_names():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM clients
            ORDER BY name
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    

    @staticmethod
    def count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM clients"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total