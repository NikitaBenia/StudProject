from app.db.base import Base


class Users(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                balance FLOAT DEFAULT 0.0,
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

        if not user:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, user))


    @Base.connection
    def get_user_by_email_and_fullname(self, cursor, fullname: str, email: str):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE email = ? AND fullname = ?
        ''', (email, fullname)).fetchone()

        if not user:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, user))


    @Base.connection
    def get_user_by_id(self, cursor, id: int):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE id = ?
        ''', (id,)).fetchone()

        if not user:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, user))

    @Base.connection
    def change_avatar(self, cursor, email: str, photo: str):
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

    @Base.connection
    def change_balance(self, cursor, email: str, balance: float):
        user = cursor.execute('''
            SELECT * FROM users
            WHERE email = ?
        ''', (email,)).fetchone()

        if not user:
            return None

        cursor.execute('''
            UPDATE users
            SET balance = ?
            WHERE email = ?
        ''', (balance, email))


users = Users()
users.create_tables()