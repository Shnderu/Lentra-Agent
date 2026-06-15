import psycopg2
from typing import Any, Dict, List, Optional


def fetch_vietnam_listings(query: Optional[dict] = None) -> List[Dict[str, Any]]:
    """
    REAL DATA LAYER v1 (PostgreSQL-backed + filters)
    """

    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        password="lentra",
        host="localhost",
        port=5432
    )

    cur = conn.cursor()

    sql = """
        SELECT
            id,
            title,
            price_vnd_mln,
            city,
            bedrooms,
            bathrooms,
            pet_friendly,
            pool,
            sea_view,
            area_m2
        FROM properties
        WHERE 1=1
    """

    params = []

    if query:

        if query.get("city"):
            sql += " AND LOWER(city) = LOWER(%s)"
            params.append(query["city"])

        if query.get("max_price"):
            sql += " AND price_vnd_mln <= %s"
            params.append(query["max_price"])

        if query.get("min_bedrooms"):
            sql += " AND bedrooms >= %s"
            params.append(query["min_bedrooms"])

        if query.get("pool") is True:
            sql += " AND pool = true"

        if query.get("sea_view") is True:
            sql += " AND sea_view = true"

        if query.get("pet_friendly") is True:
            sql += " AND pet_friendly = true"

    sql += " LIMIT 50"

    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "price": r[2],
            "city": r[3],
            "bedrooms": r[4],
            "bathrooms": r[5],
            "pet_friendly": r[6],
            "pool": r[7],
            "sea_view": r[8],
            "area": r[9],
            "source": "postgres_properties"
        }
        for r in rows
    ]
