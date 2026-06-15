from typing import Dict, Any, List
import psycopg2


def fetch_properties(conn, query: Dict[str, Any]) -> List[dict]:
    sql = """
        SELECT
            id,
            title,
            price_vnd_mln,
            deposit_vnd_mln,
            area_m2,
            bedrooms,
            bathrooms,
            pet_friendly,
            pool,
            sea_view,
            score,
            features
        FROM properties
        WHERE 1=1
    """

    params = []

    # CITY FILTER (strict)
    city = query.get("city")
    if city:
        sql += " AND LOWER(city) = LOWER(%s)"
        params.append(city)

    # BUDGET FILTER (strict)
    budget = query.get("budget_max")
    if budget is not None:
        sql += " AND price_vnd_mln <= %s"
        params.append(budget)

    sql += " ORDER BY score DESC NULLS LAST"

    with conn.cursor() as cur:
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()

        cols = [desc[0] for desc in cur.description]

    return [dict(zip(cols, row)) for row in rows]
