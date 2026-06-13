from lentra.events.stream import publish
from pyrogram import Client, filters
import os
import json

app = Client(
    "lentra_pyro",
    api_id=int(os.getenv("TG_API_ID", "0")),
    api_hash=os.getenv("TG_API_HASH", "")
)


@app.on_message(filters.chat(os.getenv("TG_CHANNELS", "DomikoVietnam").split(",")))
def handler(client, message):

    event = {
        "message_id": message.id,
        "chat_id": message.chat.id,
        "text": message.text or message.caption
    }

    publish("raw_message", event)

    print("[EVENT] published", message.id)


if __name__ == "__main__":
    print("[G-LAYER] event listener started")
    app.run()
