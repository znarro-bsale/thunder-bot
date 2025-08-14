import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
WATCH_USER_ID = os.getenv("WATCH_USER_ID")
SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID")
DEST_CHANNEL_ID = os.getenv("DEST_CHANNEL_ID")
DB_PATH = os.getenv("DB_PATH", "data/thunderteam.db")
