import psycopg2
import hashlib


def build_canonical_id(listing):
    raw = f"{listing.get('title','')}-{listing.get('city','')}-{listing.get('price','')}"
    return hashlib.sha256(raw.encode()).hexdigest()


def find_existing_cluster(canonical_id):
    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        host="127.0.0.1"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT cluster_id
        FROM tasks
        WHERE canonical_id = %s
        LIMIT 1
    """, (canonical_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else None


def assign_cluster(listing, idempotency_key):

    # LISTING MUST BE DICT
    if not isinstance(listing, dict):
        listing = {
            "id": listing,
            "idempotency_key": idempotency_key
        }

    canonical_id = build_canonical_id(listing)

    existing = find_existing_cluster(canonical_id)

    if existing:
        return existing

    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        host="127.0.0.1"
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clusters (city, canonical_signature, avg_price, min_price, max_price, listings_count)
        VALUES (%s, %s, 0, 0, 0, 0)
        RETURNING id
    """, (
        listing.get("city", ""),
        canonical_id
    ))

    cluster_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return cluster_id
