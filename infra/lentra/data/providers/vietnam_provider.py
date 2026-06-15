import psycopg2
from typing import Any, Dict, List, Optional


def fetch_vietnam_listings(query: Optional[dict] = None) -> List[Dict[str, Any]]:
    """
    REAL DATA LAYER v1 (PostgreSQL-backed)
    Замена mock → реальные properties из БД
    """

    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        password="lentra",
        host="localhost",
        port=5432
    )

    cur = conn.cursor()

    # Базовый SQL
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

    # Простейшие фильтры (MVP)
    if query:
        if query.get("city"):
            sql += " AND city = %s"
            params.append(query["city"])

        if query.get("max_price"):
            sql += " AND price_vnd_mln <= %s"
            params.append(query["max_price"])

        if query.get("min_bedrooms"):
            sql += " AND bedrooms >= %s"
            params.append(query["min_bedrooms"])

    sql += " LIMIT 50"

    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # адаптация под текущий ranking (dict-based)
    results = []

    for r in rows:
        results.append({
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
        })

    return results
