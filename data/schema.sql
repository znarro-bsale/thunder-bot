PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS team_members (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,                       -- Identificador único
  name             TEXT    NOT NULL,                                        -- Nombre del miembro
  cell             TEXT,                                                    -- Célula a la que pertenece
  slack_user_id    TEXT    NOT NULL UNIQUE,                                 -- ID de Slack
  country          TEXT,                                                    -- País de residencia
  active           INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1)),      -- Activo o no en rotación
  order_index      INTEGER NOT NULL UNIQUE,                                 -- Orden en rotación
  is_current       INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),  -- Turno actual
  assigned_count   INTEGER NOT NULL DEFAULT 0,                              -- Total asignaciones
  last_assigned_at TEXT                                                     -- Fecha última asignación
);

-- Índices útiles
CREATE INDEX IF NOT EXISTS idx_team_members_active ON team_members(active);
CREATE INDEX IF NOT EXISTS idx_team_members_current ON team_members(is_current);
