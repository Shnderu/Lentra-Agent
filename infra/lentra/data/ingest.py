import json
from lentra.data.sources.vietnam_mock import VietnamMockSource
from lentra.storage.db import get_conn

def ingest():
    source = VietnamMockSource()
    data = source.fetch()

    conn = get_conn()
    cur = conn.cursor()

    for item in data:
        cur.execute("""
            INSERT INTO processing_queue (task_type, payload, status)
            VALUES (%s, %s, 'new')
        """, (
            "search_property_vietnam",
            json.dumps(item)
        ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"[DATA INGEST] inserted={len(data)}")

if __name__ == "__main__":
    ingest()
