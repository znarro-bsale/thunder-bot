from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional, Dict, Any, Iterator

class DatabaseAdapter(ABC):

    @abstractmethod
    @contextmanager
    def connection(self) -> Iterator[Any]:
        """Context manager that returns a database connection"""
        pass

    @abstractmethod
    def execute_script(self, script: str) -> None:
        """Execute a DDL script (for table creation, etc.)"""
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute a SELECT query and return one row as dict"""
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: tuple = ()) -> list[Dict[str, Any]]:
        """Execute a SELECT query and return all rows as list of dicts"""
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = ()) -> None:
        """Execute an INSERT/UPDATE/DELETE query"""
        pass
