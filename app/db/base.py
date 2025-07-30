import sqlite3
from app.core.config import settings

# Base class for all SQLite tables, provides the connection decorator and db_path access
class Base:
    def __init__(self, db_path=settings.DATABASE_URL):
        self.db_path = db_path

    @staticmethod
    def connection(func):
        """
        Decorator that opens a SQLite connection and passes a cursor to the method.
        Requires the instance to have a 'db_path' attribute.
        """
        def wrapper(self, *args, **kwargs):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                result = func(self, cursor, *args, **kwargs)
                conn.commit()
                return result
        return wrapper
