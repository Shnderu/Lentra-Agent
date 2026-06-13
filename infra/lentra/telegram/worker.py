import os
import time
import json
import hashlib

from sqlalchemy import create_engine, text

from lentra.services.property_service import PropertyService
from lentra.parsers.property_parser import PropertyParser


# ----------------------------
# CONFIG
# ----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

POLL_INTERVAL = 2

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

service = PropertyService()
parser = PropertyParser()


# ----------------------------
# DEDUP HASH
# ----------------------------
def make_fingerprint(text_msg: str, chat_id: int) -> str:
    """
    Stable dedup key for Telegram messages
    """
    base = f"{chat_id}:{text_msg.strip().lower()}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


# ----------------------------
# SIMPLE SPAM FILTER (V1)
# ----------------------------
def is_valid_property(text: str) -> bool:
    """
    Filter out obvious non-rental content
    """

    if not text or len(text.strip()) < 10:
        return False

    t = text.lower()

    # spam / irrelevant signals
    blacklist = [
        "giveaway",
        "subscribe",
        "click here",
        "promotion",
        "crypto",
        "airdrop",
        "win money"
    ]

    if any(x in t for x in blacklist):
        return False

    # must contain at least some rental signal
    rental_signals = [
        "rent",
        "for rent",
        "studio",
        "apartment",
        "room",
        "house",
        "villa",
        "$",
        "usd",
        "vnd"
    ]

    return any(x in t for x in rental_signals)


# ----------------------------
# FETCH TASKS
# ----------------------------
def fetch_tasks(limit=10):
    with engine.begin() as conn:
        return conn.execute(text("""
            SELECT id, raw_message_id, task_type, payload
            FROM processing_queue
            WHERE status = 'new'
            ORDER BY id ASC
            LIMIT :limit
        """), {"limit": limit}).fetchall()


# ----------------------------
# RAW MESSAGE
# ----------------------------
def get_raw_message(raw_message_id):
    with engine.begin() as conn:
        return conn.execute(text("""
            SELECT id, message_id, chat_id, text, raw_json
            FROM raw_messages
            WHERE id = :id
        """), {"id": raw_message_id}).fetchone()


# ----------------------------
# UPDATE TASK
# ----------------------------
def update_task(task_id, status):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE processing_queue
            SET status = :status
            WHERE id = :id
        """), {"id": task_id, "status": status})


# ----------------------------
# DEDUP CHECK (DB LEVEL)
# ----------------------------
def already_exists(fingerprint: str) -> bool:
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT 1 FROM properties
            WHERE raw_data->>'fingerprint' = :fp
            LIMIT 1
        """), {"fp": fingerprint}).fetchone()

        return row is not None


# ----------------------------
# PROCESS TASK
# ----------------------------
def process_task(task):
    task_id, raw_message_id, task_type, payload = task

    try:
        raw = get_raw_message(raw_message_id)

        if not raw:
            update_task(task_id, "failed")
            return

        _, message_id, chat_id, text_msg, raw_json = raw

        # ----------------------------
        # FILTER LAYER (MUST PASS FIRST)
        # ----------------------------
        if not is_valid_property(text_msg):
            update_task(task_id, "done")
            print(f"[WORKER] SKIP (spam/invalid) task={task_id}")
            return

        # ----------------------------
        # DEDUP LAYER
        # ----------------------------
        fingerprint = make_fingerprint(text_msg, chat_id)

        if already_exists(fingerprint):
            update_task(task_id, "done")
            print(f"[WORKER] SKIP (duplicate) task={task_id}")
            return

        # ----------------------------
        # PARSE
        # ----------------------------
        parsed = parser.parse(text_msg)
        parsed["message_id"] = message_id

        # attach dedup fingerprint
        parsed["fingerprint"] = fingerprint

        # ----------------------------
        # DOMAIN WRITE
        # ----------------------------
        if task_type == "parse_property":
            service.process(
                text=text_msg,
                raw_json=raw_json,
                chat_id=chat_id,
                parsed=parsed
            )

        update_task(task_id, "done")
        print(f"[WORKER] DONE task={task_id}")

    except Exception as e:
        print(f"[WORKER] ERROR task={task_id}: {str(e)}")
        update_task(task_id, "failed")


# ----------------------------
# LOOP
# ----------------------------
def run():
    print("[WORKER] started")

    while True:
        tasks = fetch_tasks()

        if not tasks:
            time.sleep(POLL_INTERVAL)
            continue

        for task in tasks:
            process_task(task)


# ----------------------------
# ENTRY
# ----------------------------
if __name__ == "__main__":
    run()
