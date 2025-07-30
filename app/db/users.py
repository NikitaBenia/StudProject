from app.db.base import Base


class Users(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                profile_icon TEXT DEFAULT 'default.jpg'
            )
        ''')

    @Base.connection
    def add_user(self, cursor, fullname: str, email: str, password: str):
        from app.core.security import get_hashed_password
        hashed = get_hashed_password(password) # generating hashed password for secure in database
        user = cursor.execute('''
            SELECT * FROM users 
            WHERE email = ? AND hashed_password = ?
        ''', (email, hashed)).fetchone()

        if not user:
            cursor.execute('''
                INSERT INTO users(fullname, email, hashed_password)
                VALUES (?, ?, ?)
            ''', (fullname, email, hashed))
            return hashed

    @Base.connection
    def get_user(self, cursor, email: str):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE email = ?
        ''', (email,)).fetchone()

        if user:
            return {'fullname': user[1], 'email': user[2], 'hashed_password': user[3], 'photo': user[4]}
        return None

    @Base.connection
    def change_icon(self, cursor, email: str, photo: str):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE email = ?
        ''', (email,)).fetchone()

        if not user:
            return None

        cursor.execute('''
            UPDATE users
            SET profile_icon = ?
            WHERE email = ?
        ''', (photo, email))

users = Users()
users.create_tables()