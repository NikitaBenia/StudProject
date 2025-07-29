import sqlite3
from app.core.config import settings

class Base:
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