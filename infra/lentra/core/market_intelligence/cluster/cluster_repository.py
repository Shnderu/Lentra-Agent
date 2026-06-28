from lentra.storage.db import get_conn


def upsert_cluster(cluster_id: str, city: str, canonical_signature: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clusters (id, city, canonical_signature)
        VALUES (%s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            city = EXCLUDED.city,
            canonical_signature = EXCLUDED.canonical_signature,
            updated_at = NOW()
    """, (cluster_id, city, canonical_signature))

    conn.commit()
    cur.close()
    conn.close()


def update_cluster_stats(cluster_id: str, avg_price, min_price, max_price, count):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE clusters
        SET avg_price = %s,
            min_price = %s,
            max_price = %s,
            listings_count = %s,
            updated_at = NOW()
        WHERE id = %s
    """, (avg_price, min_price, max_price, count, cluster_id))

    conn.commit()
    cur.close()
    conn.close()
