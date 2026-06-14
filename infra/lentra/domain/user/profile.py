import psycopg2
import json

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)


def get_profile(user_id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT profile
        FROM user_profile
        WHERE user_id = %s
    """, (user_id,))

    row = cur.fetchone()
    cur.close()

    if not row:
        return {
            "budget_pref": 500,
            "cities": {},
            "interests": {}
        }

    return row[0]


def update_profile(user_id: int, delta: dict):
    profile = get_profile(user_id)

    # простое merge обновление
    for k, v in delta.items():
        profile[k] = v

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_profile (user_id, profile)
        VALUES (%s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET profile = EXCLUDED.profile
    """, (user_id, json.dumps(profile)))

    conn.commit()
    cur.close()
