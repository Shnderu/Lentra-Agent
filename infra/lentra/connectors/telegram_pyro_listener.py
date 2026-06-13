import os
import json
import asyncio
from datetime import datetime

from pyrogram import Client, filters
from sqlalchemy import create_engine, text

# ----------------------------
# CONFIG
# ----------------------------
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION_NAME = "lentra_pyro"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/lentra"
)

TARGET_CHANNELS = os.getenv(
    "TG_CHANNELS",
    "DomikoVietnam"
).split(",")

# ----------------------------
# DB ENGINE
# ----------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ----------------------------
# PYROGRAM CLIENT
# ----------------------------
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)

# ----------------------------
# NORMALIZATION
# ----------------------------
def normalize_message(message):
    text = message.text or message.caption or ""

    return {
        "message_id": message.id,
        "chat_id": message.chat.id,
        "chat_title": getattr(message.chat, "title", None),
        "text": text,
        "raw_json": json.dumps({
            "id": message.id,
            "date": str(message.date),
            "chat_id": message.chat.id
        }, ensure_ascii=False),
        "ingested_at": datetime.utcnow()
    }

# ----------------------------
# POSTGRES INSERT (RAW LAYER)
# ----------------------------
def insert_raw_message(payload: dict):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO raw_messages
            (message_id, chat_id, chat_title, text, raw_json, ingested_at, status)
            VALUES
            (:message_id, :chat_id, :chat_title, :text, :raw_json, :ingested_at, 'new')
            ON CONFLICT (message_id, chat_id) DO NOTHING
        """), payload)

# ----------------------------
# QUEUE TASK CREATION
# ----------------------------
def push_to_queue(message_id: int, chat_id: int):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO processing_queue
            (raw_message_id, task_type, payload, status, created_at)
            VALUES
            (
                (SELECT id FROM raw_messages WHERE message_id=:message_id AND chat_id=:chat_id),
                'parse_property',
                :payload,
                'new',
                NOW()
            )
            ON CONFLICT DO NOTHING
        """), {
            "message_id": message_id,
            "chat_id": chat_id,
            "payload": json.dumps({"type": "parse_property"})
        })

# ----------------------------
# HANDLER
# ----------------------------
@app.on_message(filters.chat(TARGET_CHANNELS))
async def handler(client, message):
    try:
        payload = normalize_message(message)

        # 1. save raw
        insert_raw_message(payload)

        # 2. push task
        push_to_queue(payload["message_id"], payload["chat_id"])

        print("[INGEST] OK:", payload["message_id"])

    except Exception as e:
        print("[ERROR]", str(e))

# ----------------------------
# MAIN LOOP
# ----------------------------
async def main():
    print("[LENTRA] Listener starting...")
    print("[LENTRA] Channels:", TARGET_CHANNELS)

    await app.start()

    print("[LENTRA] ACTIVE PIPELINE V1")

    while True:
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
