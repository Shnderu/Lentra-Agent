import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    try:
        with open("/opt/lentra/infra/.env") as f:
            for line in f:
                if line.startswith("BOT_TOKEN="):
                    BOT_TOKEN = line.strip().split("=", 1)[1]
                    break
    except Exception:
        pass


def send_telegram(chat_id: int, text: str, keyboard=None):

    if not BOT_TOKEN:
        print("[TELEGRAM ERROR] BOT_TOKEN not found")
        return False

    payload = {
        "chat_id": chat_id,
        "text": text or "Сообщение без текста"
    }

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=15
        )

        print(f"[TELEGRAM] status={r.status_code}")
        print(r.text)

        return r.status_code == 200

    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False
