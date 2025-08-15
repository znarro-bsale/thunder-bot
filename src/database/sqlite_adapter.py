import sqlite3
from contextlib import contextmanager
from typing import Optional, Dict, Any, Iterator
from .adapter import DatabaseAdapter
from ..config import SQLITE_DB_PATH

class SqliteAdapter(DatabaseAdapter):
    
    def __init__(self):
        self.db_path = SQLITE_DB_PATH
    
    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def execute_script(self, script: str) -> None:
        with self.connection() as conn:
            conn.executescript(script)
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        with self.connection() as conn:
            row = conn.execute(query, params).fetchone()
            return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> list[Dict[str, Any]]:
        with self.connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    def execute(self, query: str, params: tuple = ()) -> None:
        with self.connection() as conn:
            conn.execute(query, params)