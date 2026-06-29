import os

BOT_TOKEN = os.getenv("LENTRA_BOT_TOKEN", "")

if not BOT_TOKEN:
    raise RuntimeError("LENTRA_BOT_TOKEN is not set")
