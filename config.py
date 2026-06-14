import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Required Telegram Credentials ---
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    STRING_SESSION = os.getenv("STRING_SESSION")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))

    # --- Database & Media ---
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "monkeydluffy")
    CATBOX_USERHASH = os.getenv("CATBOX_USERHASH", None)
    START_IMAGE_URL = os.getenv("START_IMAGE_URL", "https://files.catbox.moe/yourimage.jpg")
    STICKER_ID = os.getenv("STICKER_ID", "CAACAgIAAxkBAAEBEXAMPLE")

    # --- Bot Logic Settings ---
    AUTO_LEAVE = int(os.getenv("AUTO_LEAVE", 300))
    DOWNLOAD_PATH = "downloads/"

    # --- Web Dashboard Settings ---
    DASHBOARD_USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
    DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "changeme123")
    DASHBOARD_PORT = int(os.getenv("PORT", 8000))

    @classmethod
    def validate(cls):
        if not cls.API_ID or cls.API_ID == 0:
            raise ValueError("API_ID is missing or invalid")
        if not cls.API_HASH:
            raise ValueError("API_HASH is missing")
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is missing")
        if not cls.STRING_SESSION:
            raise ValueError("STRING_SESSION is missing")
        if not cls.OWNER_ID:
            raise ValueError("OWNER_ID is missing")
        print("✅ All required configuration variables are present.")
