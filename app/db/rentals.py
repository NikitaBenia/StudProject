import sqlite3

from app.db.base import Base


class Rentals(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (car_id) REFERENCES cars(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')


    @Base.connection
    def add_rental(self, cursor, car_id: int, user_id: int, start_time: str, end_time: str):
        try:
            cursor.execute('''
                INSERT INTO rentals (car_id, user_id, start_time, end_time)
                VALUES (?, ?, ?, ?)
            ''', (car_id, user_id, start_time, end_time))
            return True
        except sqlite3.IntegrityError:
            return False


    @Base.connection
    def select_users_rentals(self, cursor, user_id: int):
        cursor.execute('''
            SELECT rentals.*, cars.title, cars.price, cars.photo
            FROM rentals
            JOIN cars ON rentals.car_id = cars.id
            WHERE rentals.user_id = ?
        ''', (user_id,))

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]
        return results


    @Base.connection
    def update_expired_rentals(self, cursor, user_id, today):
        cursor.execute("""
            UPDATE rentals
            SET status = 'finished'
            WHERE user_id = ?
              AND status = 'active'
              AND end_time <= ?
        """, (user_id, today))

rentals = Rentals()
rentals.create_tables()