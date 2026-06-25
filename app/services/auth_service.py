import bcrypt

from app.database.database import Database


class AuthService:

    def __init__(self):

        self.db = Database()

        self.create_admin()

    def create_admin(self):

        self.db.cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            ("admin",)
        )

        user = self.db.cursor.fetchone()

        if user is None:

            password = bcrypt.hashpw(
                "admin".encode(),
                bcrypt.gensalt()
            )

            self.db.cursor.execute(
                """
                INSERT INTO users
                (username, password, role)

                VALUES (?, ?, ?)
                """,
                (
                    "admin",
                    password.decode(),
                    "admin"
                )
            )

            self.db.commit()