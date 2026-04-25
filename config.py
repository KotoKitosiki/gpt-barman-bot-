import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = "deepseek/deepseek-chat-v3-0324:free"
    YOO_MONEY_CLIENT_ID: str = os.getenv("YOO_MONEY_CLIENT_ID", "")
    YOO_MONEY_WALLET: str = os.getenv("YOO_MONEY_WALLET", "")
    ADMIN_TELEGRAM_ID: str = os.getenv("ADMIN_TELEGRAM_ID", "")
    FREE_DAILY_LIMIT: int = 3

settings = Settings()
