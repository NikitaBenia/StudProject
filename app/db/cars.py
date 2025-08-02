from app.db.base import Base


class Cars(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                description TEXT NULLABLE,
                city TEXT NOT NULL,
                price FLOAT NOT NULL,
                photo TEXT NULLABLE
            )
        ''')


    @Base.connection
    def select_all_cars(self, cursor):
        cars = cursor.execute('SELECT * FROM cars').fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, car)) for car in cars]


    @Base.connection
    def select_car_by_title(self, cursor, title: str):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE title = ?
        ''', (title,)).fetchone()

        if not car:
            return False
        return True


    @Base.connection
    def select_car_by_id(self, cursor, id: int):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE id = ?
        ''', (id,)).fetchone()

        if not car:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, car))


    @Base.connection
    def add_car(self, cursor, title: str, description: str, city: str, price: float, photo: str):
        car = cursor.execute('''
            SELECT * FROM cars
            WHERE title = ?
        ''', (title,)).fetchone()

        if not car:
            car_id = cursor.execute('''
                INSERT INTO cars(title, city, description, price, photo)
                VALUES (?, ?, ?, ?, ?)
                RETURNING id
            ''', (title, city, description, price, photo)).fetchone()[0]
            return car_id


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