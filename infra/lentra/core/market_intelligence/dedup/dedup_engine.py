import hashlib
import json
import uuid

from lentra.storage.db import get_conn
from lentra.core.market_intelligence.cluster.cluster_repository import upsert_cluster


def build_canonical_id(listing: dict) -> str:
    base = {
        "title": listing.get("title", "").strip().lower(),
        "city": listing.get("city", "").strip().lower(),
        "location": listing.get("location", "").strip().lower(),
        "price": str(listing.get("price", 0)),
        "currency": listing.get("currency", "USD").upper(),
        "source": listing.get("source", "")
    }

    raw = json.dumps(base, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def find_existing_cluster(canonical_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT cluster_id
        FROM tasks
        WHERE canonical_id = %s
          AND cluster_id IS NOT NULL
        LIMIT 1
    """, (canonical_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else None


def assign_cluster(listing: dict, canonical_id: str):
    existing = find_existing_cluster(canonical_id)

    if existing:
        return existing

    cluster_id = str(uuid.uuid4())

    # persist NEW cluster immediately
    upsert_cluster(
        cluster_id=cluster_id,
        city=listing.get("city", ""),
        canonical_signature=canonical_id
    )

    return cluster_id
