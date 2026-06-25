from app.database.database import get_connection


class AuthController:

    def login(self, username, password):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return None

        if password == user["password"]:
            return user

        return None