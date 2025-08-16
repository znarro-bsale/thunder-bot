from datetime import datetime
from .database.factory import get_db

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
    db_adapter = get_db()
    db_adapter.execute_script(ddl)

def get_members():
    db_adapter = get_db()
    return db_adapter.fetch_all(
        "SELECT * FROM team_members WHERE active = 1 ORDER BY order_index ASC"
    )

def get_member_by_slack_id(slack_user_id):
    db_adapter = get_db()
    return db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE slack_user_id = ? LIMIT 1",
        (slack_user_id,)
    )

def get_current():
    db_adapter = get_db()
    current = db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE is_current = 1 LIMIT 1"
    )
    if current:
        return current
    return db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE active = 1 ORDER BY order_index ASC LIMIT 1"
    )

def get_next_after(order_index: int):
    db_adapter = get_db()
    nxt = db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE active = 1 AND order_index > ? ORDER BY order_index ASC LIMIT 1",
        (order_index,),
    )
    if nxt:
        return nxt
    return db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE active = 1 ORDER BY order_index ASC LIMIT 1"
    )

def get_previous_before(order_index: int):
    db_adapter = get_db()
    prev = db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE active = 1 AND order_index < ? ORDER BY order_index DESC LIMIT 1",
        (order_index,),
    )
    if prev:
        return prev
    return db_adapter.fetch_one(
        "SELECT * FROM team_members WHERE active = 1 ORDER BY order_index DESC LIMIT 1"
    )


def next_turn():
    """Pasa el turno al siguiente activo"""
    curr = get_current()
    if not curr:
        return None # No hay miembros activos

    next = get_next_after(curr["order_index"])
    if not next:
        return None # No hay miembros activos

    now = datetime.utcnow().isoformat()

    db_adapter = get_db()
    # Marcar next como current y actualizar métricas
    db_adapter.execute("""
        UPDATE team_members
        SET is_current = 0,
            assigned_count = IIF(assigned_count - 1 > 0, assigned_count - 1, 0)
        WHERE is_current = 1
    """)
    db_adapter.execute("""
        UPDATE team_members
        SET is_current = 1,
            assigned_count = assigned_count + 1,
            last_assigned_at = ? WHERE id = ?
    """, (now, next["id"]))

    return next

def previous_turn():
    """Pasa el turno al anterior activo"""
    curr = get_current()
    if not curr:
        return None # No hay miembros activos

    prev = get_previous_before(curr["order_index"])
    if not prev:
        return None # No hay miembros activos

    now = datetime.utcnow().isoformat()

    db_adapter = get_db()
    # Marcar prev como current y actualizar métricas
    db_adapter.execute("""
        UPDATE team_members
        SET is_current = 0, assigned_count = IIF(assigned_count - 1 > 0, assigned_count - 1, 0)
        WHERE is_current = 1
    """)
    db_adapter.execute("""
        UPDATE team_members
        SET is_current = 1,
            assigned_count = assigned_count + 1,
            last_assigned_at = ? WHERE id = ?
    """, (now, prev["id"]))

    return prev

def set_member_state(id, state):
    db_adapter = get_db()
    try:
        current = get_current()
        db_adapter.execute("""
            UPDATE team_members
            SET active = ?
            WHERE id = ?
        """, (state, id))
        return True
    except Exception:
        return False
