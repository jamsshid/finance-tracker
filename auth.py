import hashlib
from utils.db import get_connection


class AuthManager:

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email: str, password: str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (email, password) VALUES (%s, %s)",
                    (email, self.hash_password(password)),
                )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()

    def login_user(self, email: str, password: str) -> "int | None":
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM users WHERE email = %s AND password = %s",
                    (email, self.hash_password(password)),
                )
                row = cur.fetchone()
            return row[0] if row else None
        finally:
            conn.close()
