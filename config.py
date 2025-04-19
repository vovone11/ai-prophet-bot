from dotenv import load_dotenv
import os
import os

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
DB_PATH = "ai_prophet.db"
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
