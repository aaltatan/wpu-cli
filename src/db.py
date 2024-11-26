import sqlite3
from typing import Self
from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, path: str = "app.db") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = self.default_factory
        self.cursor = self.conn.cursor()
        self._create_tables()

    @abstractmethod
    def _create_tables(self) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close_connection()

    def close_connection(self) -> None:
        self.conn.close()

    def default_factory(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        headers = [column[0] for column in cursor.description]
        return {k: v for k, v in zip(headers, row)}
