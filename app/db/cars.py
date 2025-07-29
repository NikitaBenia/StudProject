from app.db.base import Base


class Cars(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                price FLOAT NOT NULL,
                photo TEXT NULLABLE
            )
        ''')

    @Base.connection
    def select_car(self, cursor, title: str):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE title = ?
        ''', (title,)).fetchone()

        if not car:
            return None
        return {'title': car[1], 'price': car[2], 'photo': car[3]}

    @Base.connection
    def add_car(self, cursor, title: str, price: float, photo: str):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE title = ?
        ''', (title,)).fetchone()

        if not car:
            cursor.execute('''
                INSERT INTO cars(title, price, photo)
                VALUES (?, ?, ?)
            ''', (title, price, photo))

    @Base.connection
    def remove_car(self, cursor, id: int):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE id = ?
        ''', (id,)).fetchone()

        if car:
            cursor.execute('''
                DELETE FROM cars
                WHERE id = ?
            ''', (id,)).fetchone()

cars = Cars()
cars.create_tables()