import sqlite3
from app.core.config import settings
from app.core.security import get_hashed_password


class Users:
    def __init__(self, db_path=settings.DATABASE_URL):
        self.db_path = db_path

    @staticmethod
    def connection(func):
        def wrapper(self, *args, **kwargs):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                conn.commit()
                return func(self, cursor, *args, **kwargs)
        return wrapper

    @connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
        ''')

    @connection
    def add_user(self, cursor, username: str, password: str):
        hashed = get_hashed_password(password)
        user = cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND hashed_password = ?
        ''', (username, hashed)).fetchone()

        if not user:
            cursor.execute('''
                INSERT INTO users(username, hashed_password)
                VALUES (?, ?)
            ''', (username, hashed))

    @connection
    def get_user(self, cursor, username: str):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE username = ?
        ''', (username,)).fetchone()

        if user:
            return {'username': user[1], 'hashed_password': user[2]}
        return None


users = Users()
users.create_tables()