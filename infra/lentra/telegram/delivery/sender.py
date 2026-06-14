import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_telegram(chat_id: int, text: str, keyboard=None):

    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if keyboard:
        payload["reply_markup"] = {
            "inline_keyboard": keyboard
        }

    r = requests.post(f"{API_URL}/sendMessage", json=payload)

    if r.status_code != 200:
        print("[TELEGRAM ERROR]", r.text)
        return False

    return True
