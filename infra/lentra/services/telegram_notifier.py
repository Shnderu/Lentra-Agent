from pyrogram import Client
import os

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION = "lentra_pyro"


class TelegramNotifier:

    def __init__(self):
        self.app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

    def start(self):
        self.app.start()

    def stop(self):
        self.app.stop()

    def send(self, user_id: int, text: str):
        try:
            self.app.send_message(user_id, text)
            print("[PUSH] sent to", user_id)
        except Exception as e:
            print("[PUSH ERROR]", e)
