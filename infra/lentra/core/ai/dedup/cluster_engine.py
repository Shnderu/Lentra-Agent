from lentra.storage.db import get_conn


def get_or_create_cluster(canonical_id: str, city: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM listing_clusters
        WHERE canonical_id = %s
    """, (canonical_id,))

    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("""
        INSERT INTO listing_clusters (canonical_id, city)
        VALUES (%s, %s)
        RETURNING id
    """, (canonical_id, city))

    cluster_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return cluster_id


def attach_listing_to_cluster(listing_id: str, canonical_id: str, city: str):
    conn = get_conn()
    cur = conn.cursor()

    cluster_id = get_or_create_cluster(canonical_id, city)

    cur.execute("""
        INSERT INTO listing_cluster_map (listing_id, cluster_id, canonical_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (listing_id) DO UPDATE
        SET cluster_id = EXCLUDED.cluster_id
    """, (listing_id, cluster_id, canonical_id))

    conn.commit()
    cur.close()
    conn.close()

    return cluster_id
