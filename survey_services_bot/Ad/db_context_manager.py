import mysql
from mysql.connector.cursor_cext import CMySQLCursor


class DBContextManager:
    # Unused
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self) -> CMySQLCursor:
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
