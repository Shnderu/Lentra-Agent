import os
import time
import asyncio

from telethon import TelegramClient

from lentra.services.alert_matcher import AlertMatcher

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

client = TelegramClient("alert_bot", API_ID, API_HASH)

matcher = AlertMatcher()


def format_item(r):
    return (
        f"🚨 NEW MATCH\n\n"
        f"{r.description}\n\n"
        f"💰 {r.price} {r.currency}\n"
        f"⭐ {r.confidence}"
    )


async def run():
    await client.start(bot_token=BOT_TOKEN)
    print("[ALERT] worker started")

    while True:
        matches = matcher.get_new_matches()

        for alert_id, chat_id, r in matches:
            try:
                await client.send_message(chat_id, format_item(r))

                # ----------------------------
                # MARK AS SENT
                # ----------------------------
                with matcher.engine.begin() as conn:
                    conn.execute("""
                        INSERT INTO alert_matches (alert_id, property_id)
                        VALUES (:alert_id, :property_id)
                    """, {
                        "alert_id": alert_id,
                        "property_id": r.id
                    })

            except Exception as e:
                print("[ALERT] send error:", e)

        time.sleep(10)


if __name__ == "__main__":
    asyncio.run(run())
