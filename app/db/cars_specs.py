from app.db.base import Base


class CarsSpecs(Base):
    @Base.connection
    def create_tables(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars_specs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                engine STRING,
                horsepower INTEGER,
                torque INTEGER,
                mph FLOAT,
                top_speed INTEGER,
                transmission STRING,
                drivetrain STRING,
                hybrid_system STRING,
                technology STRING,
                audio STRING,
                interior STRING,
                lighting STRING,
                comfort STRING,
                exterior STRING,
                FOREIGN KEY (car_id) REFERENCES cars(id)
            )
        ''')

    @Base.connection
    def select_specs_by_car_id(self, cursor, car_id: int):
        specs = cursor.execute('SELECT * FROM cars_specs WHERE car_id = ?', (car_id,)).fetchone()
        if not specs:
            return None
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, specs))

    @Base.connection
    def add_specs(self, cursor, car_id: int, engine: str, horsepower: int, torque: int, mph: float,
                  top_speed: int, transmission: str, drivetrain: str, hybrid_system: str,
                  technology: str, audio: str, interior: str, lighting: str,
                  comfort: str, exterior: str):
        cursor.execute('''
            INSERT INTO cars_specs(
                car_id, engine, horsepower, torque, mph, top_speed,
                transmission, drivetrain, hybrid_system, technology,
                audio, interior, lighting, comfort, exterior
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            car_id, engine, horsepower, torque, mph, top_speed,
            transmission, drivetrain, hybrid_system, technology,
            audio, interior, lighting, comfort, exterior
        ))

    @Base.connection
    def remove_specs(self, cursor, car_id: int):
        cursor.execute('''
            DELETE FROM cars_specs
            WHERE car_id = ?
        ''', (car_id,))


cars_specs = CarsSpecs()
cars_specs.create_tables()