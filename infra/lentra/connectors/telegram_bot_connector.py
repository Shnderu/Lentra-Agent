import os
import requests

class TelegramBotConnector:
    def __init__(self):
        self.token = os.getenv("BOT_TOKEN")
        self.base = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self, offset=None):
        url = f"{self.base}/getUpdates"
        params = {"timeout": 10}
        if offset:
            params["offset"] = offset

        r = requests.get(url, params=params)
        return r.json()

    def fetch_messages(self):
        data = self.get_updates()
        if not data.get("ok"):
            return []

        messages = []
        for item in data["result"]:
            msg = item.get("message")
            if msg:
                messages.append({
                    "text": msg.get("text"),
                    "chat_id": msg["chat"]["id"],
                    "date": msg.get("date")
                })

        return messages
