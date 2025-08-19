import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

def parse_channel_list(channel_str: str) -> list[str]:
    """Parsea IDs de canales si hay más de uno"""
    if not channel_str:
        return []
    return [ch.strip() for ch in channel_str.split(',') if ch.strip()]

# Slack Configuration
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
TEAM_ID = os.getenv("TEAM_ID")
SOURCE_CHANNEL_IDS = parse_channel_list(os.getenv("SOURCE_CHANNEL_IDS", ""))
DEST_CHANNEL_IDS = parse_channel_list(os.getenv("DEST_CHANNEL_IDS", ""))
ALLOWED_COMMAND_CHANNEL = os.getenv("ALLOWED_COMMAND_CHANNEL", "")

# Discord Configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

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
