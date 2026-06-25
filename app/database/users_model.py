from app.database.database import get_connection
import bcrypt

class UsersModel:

    @staticmethod
    def create_table():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER DEFAULT 1
            )
        """)

        conn.commit()

        conn.close()

    @staticmethod
    def create_default_admin():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            ("admin",)
        )

        user = cursor.fetchone()

        if not user:

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?)
            """, (
                "admin",
                "admin",
                "admin"
            ))

            conn.commit()

        conn.close()

    @staticmethod
    def authenticate(username, password):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            AND active = 1
        """, (
            username,
            password
        ))

        user = cursor.fetchone()

        conn.close()

        return user
    

    @staticmethod
    def get_all():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            ORDER BY username
        """)

        users = cursor.fetchall()

        conn.close()

        return users
    

    @staticmethod
    def get_by_id(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

        conn.close()

        return user
    

    @staticmethod
    def create(username, password, role):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (
                username,
                password,
                role
            )
            VALUES (?, ?, ?)
        """, (
            username,
            password,
            role
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def update(user_id, username, password, role):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET
                username = ?,
                password = ?,
                role = ?
            WHERE id = ?
        """, (
            username,
            password,
            role,
            user_id
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def toggle_active(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT active FROM users WHERE id = ?",
            (user_id,)
        )

        current = cursor.fetchone()

        new_value = 0 if current["active"] == 1 else 1

        cursor.execute("""
            UPDATE users
            SET active = ?
            WHERE id = ?
        """, (
            new_value,
            user_id
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def delete(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id != 1 AND id = ?",
            (user_id,)
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_barbers():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role = 'barber'
            AND active = 1
            ORDER BY username
        """)

        users = cursor.fetchall()

        conn.close()

        return users
    


    @staticmethod
    def count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total
    

    @staticmethod
    def barber_count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role = 'barber'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    


    @staticmethod
    def get_by_username(username):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        return user
    

    @staticmethod
    def change_password(user_id, password):

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            hashed,
            user_id
        ))

        conn.commit()
        conn.close()