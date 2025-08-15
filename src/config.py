import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# Slack Configuration
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
WATCH_USER_ID = os.getenv("WATCH_USER_ID")
SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID")
DEST_CHANNEL_ID = os.getenv("DEST_CHANNEL_ID")

# Database Configuration
class DatabaseType(Enum):
    SQLITE = "sqlite"
    TURSO = "turso"

# Current DB
DATABASE_TYPE = DatabaseType.TURSO

# SQLite Configuration
SQLITE_DB_PATH = os.getenv("DB_PATH", "data/thunderteam.db")

# Turso Configuration
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
