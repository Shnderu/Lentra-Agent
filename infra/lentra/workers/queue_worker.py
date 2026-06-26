import time
from sqlalchemy import create_engine, text

from lentra.parsers.property_parser import get_property_by_raw_message
from lentra.services.telegram_notifier import TelegramNotifier
from lentra.ml.vector_search import search
from lentra.services.ranking_ensemble import rank

DATABASE_URL = "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

notifier = TelegramNotifier()
notifier.start()


def process():
    with engine.begin() as conn:
        task = conn.execute(text("""
            SELECT id, raw_message_id, payload
            FROM processing_queue
            WHERE status = 'new'
            ORDER BY id ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """)).fetchone()

        if not task:
            return

        conn.execute(text("""
            UPDATE processing_queue
            SET status = 'processing'
            WHERE id = :id
        """), {"id": task.id})

    property_obj = get_property_by_raw_message(task.raw_message_id)

    if not property_obj:
        return

    candidates = search(property_obj.title or "", limit=20)

    ranked = rank([property_obj])

    # 🔥 FIX: достаём реальный chat_id из payload
    chat_id = None
    try:
        import json
        payload = json.loads(task.payload) if task.payload else {}
        chat_id = payload.get("chat_id")
    except Exception:
        chat_id = None

    if not chat_id:
        chat_id = 928857415  # fallback

    for r in ranked:
        notifier.send(chat_id, f"🏠 {r['title']} | score={r['score']:.3f}")

    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE processing_queue
            SET status = 'done'
            WHERE id = :id
        """), {"id": task.id})


if __name__ == "__main__":
    print("[WORKER] F-layer FULL SYSTEM ACTIVE")
    while True:
        process()
        time.sleep(2)
