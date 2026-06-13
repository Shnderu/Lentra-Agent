import os
import json
from datetime import datetime

from pyrogram import Client
from sqlalchemy import create_engine, text as sql_text

API_ID = int(os.getenv("TG_API_ID", "34837463"))
API_HASH = os.getenv("TG_API_HASH", "660e4e614f3ebc98d02284ef4cffec19")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = Client(
    "lentra_pyro",
    api_id=API_ID,
    api_hash=API_HASH
)

# -------------------------
# HANDLER
# -------------------------
@app.on_message()
async def handler(client, message):
    try:
        print("[DEBUG] TRIGGERED:", message.id)

        msg_text = message.text or message.caption or ""

        with engine.begin() as conn:

            raw_id = conn.execute(sql_text("""
                INSERT INTO raw_messages
                (message_id, chat_id, chat_title, text, raw_json, ingested_at, status)
                VALUES
                (:message_id, :chat_id, :chat_title, :text, :raw_json, :ingested_at, 'new')
                ON CONFLICT (message_id, chat_id)
                DO UPDATE SET text = EXCLUDED.text
                RETURNING id
            """), {
                "message_id": message.id,
                "chat_id": message.chat.id,
                "chat_title": getattr(message.chat, "title", None),
                "text": msg_text,
                "raw_json": json.dumps({
                    "id": message.id,
                    "chat_id": message.chat.id
                }),
                "ingested_at": datetime.utcnow()
            }).scalar()

            conn.execute(sql_text("""
                INSERT INTO processing_queue
                (raw_message_id, task_type, payload, status, created_at)
                VALUES
                (:raw_message_id, :task_type, :payload, 'new', NOW())
            """), {
                "raw_message_id": raw_id,
                "task_type": "parse_property",
                "payload": json.dumps({"type": "parse_property"})
            })

        print("[INGEST] OK")
        print("[QUEUE] CREATED:", raw_id)

    except Exception as e:
        print("[ERROR]", str(e))


# -------------------------
# MAIN
# -------------------------
def main():
    print("[LENTRA] Listener starting...")
    app.run()


if __name__ == "__main__":
    main()
