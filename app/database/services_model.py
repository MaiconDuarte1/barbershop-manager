from app.database.database import get_connection


class ServicesModel:

    @staticmethod
    def create_table():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                duration INTEGER,
                description TEXT,
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
            FROM services
            ORDER BY name
        """)

        services = cursor.fetchall()

        conn.close()

        return services

    @staticmethod
    def create(name, price, duration, description):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO services (
                name,
                price,
                duration,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            price,
            duration,
            description
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(service_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM services WHERE id = ?",
            (service_id,)
        )

        service = cursor.fetchone()

        conn.close()

        return service

    @staticmethod
    def update(service_id, name, price, duration, description):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE services
            SET
                name = ?,
                price = ?,
                duration = ?,
                description = ?
            WHERE id = ?
        """, (
            name,
            price,
            duration,
            description,
            service_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(service_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM services WHERE id = ?",
            (service_id,)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def search(text):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM services
            WHERE name LIKE ?
            ORDER BY name
        """, (
            f"%{text}%",
        ))

        services = cursor.fetchall()

        conn.close()

        return services
    

    @staticmethod
    def get_names():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM services
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
            "SELECT COUNT(*) FROM services"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total
    


    @staticmethod
    def most_used():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.name,
                COUNT(*) AS total

            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status IN (
                'Concluído',
                'Pago'
            )

            GROUP BY s.name

            ORDER BY total DESC

            LIMIT 5
        """)

        data = cursor.fetchall()

        conn.close()

        return data