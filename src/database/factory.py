from .adapter import DatabaseAdapter
from .sqlite_adapter import SqliteAdapter
from ..config import DATABASE_TYPE, DatabaseType

def get_database_adapter() -> DatabaseAdapter:
    """Factory function to get the configured database adapter"""
    if DATABASE_TYPE == DatabaseType.SQLITE:
        return SqliteAdapter()
    elif DATABASE_TYPE == DatabaseType.TURSO:
        from .turso_adapter import TursoAdapter
        return TursoAdapter()
    else:
        raise ValueError(f"Unsupported database type: {DATABASE_TYPE}")

# Global instance - singleton pattern
_db_adapter: DatabaseAdapter = None

def get_db() -> DatabaseAdapter:
    """Get the database adapter instance (singleton)"""
    global _db_adapter
    if _db_adapter is None:
        _db_adapter = get_database_adapter()
    return _db_adapter