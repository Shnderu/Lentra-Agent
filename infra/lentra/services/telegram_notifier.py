import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class TelegramNotifier:

    def __init__(self):
        if not BOT_TOKEN:
            print("[NOTIFIER ERROR] BOT_TOKEN is empty")

    def start(self):
        print("[NOTIFIER] HTTP MODE READY")

    def stop(self):
        pass

    def send(self, user_id: int, text: str):
        try:
            r = requests.post(
                f"{BASE_URL}/sendMessage",
                json={
                    "chat_id": user_id,
                    "text": text
                },
                timeout=(3, 10)
            )

            print("[PUSH STATUS]", r.status_code, r.text)

        except Exception as e:
            print("[PUSH ERROR]", repr(e))
