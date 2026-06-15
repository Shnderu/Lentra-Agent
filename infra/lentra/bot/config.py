import os
from dotenv import load_dotenv

load_dotenv("/opt/lentra/infra/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
