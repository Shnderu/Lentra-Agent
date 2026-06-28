from lentra.storage.db import get_conn


def get_or_create_area(city: str, area_name: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM area_profiles
        WHERE city = %s AND area_name = %s
    """, (city, area_name))

    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("""
        INSERT INTO area_profiles (city, area_name)
        VALUES (%s, %s)
        RETURNING id
    """, (city, area_name))

    area_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return area_id


def attach_area(listing_id: str, city: str, area_name: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO listing_area_map (listing_id, area_name, city)
        VALUES (%s, %s, %s)
        ON CONFLICT (listing_id)
        DO UPDATE SET area_name = EXCLUDED.area_name
    """, (listing_id, area_name, city))

    conn.commit()
    cur.close()
    conn.close()

    return area_name


def update_area_scores(area_name: str, city: str):
    conn = get_conn()
    cur = conn.cursor()

    # базовая агрегация из listing (proxy signals)
    cur.execute("""
        SELECT COUNT(*)
        FROM tasks t
        JOIN listing_area_map m ON m.listing_id = t.id
        WHERE m.area_name = %s
    """, (area_name,))

    count = cur.fetchone()[0]

    # простая эвристика (MVP)
    internet = min(10, count * 0.3)
    noise = max(1, 10 - count * 0.2)
    expats = min(10, count * 0.5)
    infra = min(10, count * 0.4)

    area_score = (internet * 0.3 + expats * 0.3 + infra * 0.3 + (10 - noise) * 0.1)

    cur.execute("""
        UPDATE area_profiles
        SET internet_score = %s,
            noise_score = %s,
            expat_density = %s,
            infra_score = %s,
            area_score = %s,
            updated_at = NOW()
        WHERE area_name = %s
    """, (internet, noise, expats, infra, area_score, area_name))

    conn.commit()
    cur.close()
    conn.close()
