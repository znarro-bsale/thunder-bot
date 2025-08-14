import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from config import DB_PATH

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    ddl = """
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS team_members (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,                       -- Identificador único
      name             TEXT    NOT NULL,                                        -- Nombre del miembro
      cell             TEXT,                                                    -- Célula a la que pertenece
      slack_user_id    TEXT    NOT NULL UNIQUE,                                 -- ID de Slack
      active           INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1)),      -- Activo o no en rotación
      order_index      INTEGER NOT NULL UNIQUE,                                 -- Orden en rotación
      is_current       INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),  -- Turno actual
      assigned_count   INTEGER NOT NULL DEFAULT 0,                              -- Total asignaciones
      last_assigned_at TEXT                                                     -- Fecha última asignación
    );
    CREATE INDEX IF NOT EXISTS idx_team_members_active ON team_members(active);
    CREATE INDEX IF NOT EXISTS idx_team_members_current ON team_members(is_current);
    """
    with db() as conn:
        conn.executescript(ddl)

def get_current():
    with db() as conn:
        return conn.execute(
            "SELECT * FROM team_members WHERE is_current = 1 LIMIT 1"
        ).fetchone()

def get_next_after(order_index: int):
    with db() as conn:
        nxt = conn.execute(
            "SELECT * FROM team_members WHERE active = 1 AND order_index > ? ORDER BY order_index ASC LIMIT 1",
            (order_index,),
        ).fetchone()
        if nxt:
            return nxt
        return conn.execute(
            "SELECT * FROM team_members WHERE active = 1 ORDER BY order_index ASC LIMIT 1"
        ).fetchone()

def advance_rotation_and_mark_assigned():
    """Pasa el turno al siguiente activo, actualiza is_current, assigned_count y last_assigned_at."""
    curr = get_current()
    if not curr:
        nxt = get_next_after(-10**9)  # Empezar desde el primero activo
    else:
        nxt = get_next_after(curr["order_index"])
    if not nxt:
        return None

    now = datetime.utcnow().isoformat()
    with db() as conn:
        # Quitar el current previo
        conn.execute("UPDATE team_members SET is_current = 0 WHERE is_current = 1")
        # Marcar next como current y actualizar métricas
        conn.execute("""
            UPDATE team_members
            SET is_current = 1,
                assigned_count = assigned_count + 1,
                last_assigned_at = ?
            WHERE id = ?
        """, (now, nxt["id"]))
    return nxt
