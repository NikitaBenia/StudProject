from app.core.security import get_hashed_password
from app.db.base import Base


class Users(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                profile_icon TEXT DEFAULT 'default.png'
            )
        ''')

    @Base.connection
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

    @Base.connection
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