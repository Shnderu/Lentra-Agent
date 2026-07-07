import psycopg2
import json

from lentra.ml.embedding_service import EmbeddingService


DB = {
    "dbname": "lentra",
    "user": "lentra_user",
    "password": "lentra_pass",
    "host": "localhost",
    "port": 5432
}

service = EmbeddingService()


def main():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("SELECT id, title, features, area_m2 FROM properties")
    rows = cur.fetchall()

    for r in rows:
        pid, title, features, area = r

        prop = {
            "title": title,
            "features": features or {},
            "area_m2": area
        }

        emb = service.encode_property(prop)

        cur.execute(
            "UPDATE properties SET embedding = %s WHERE id = %s",
            (json.dumps(emb), pid)
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
