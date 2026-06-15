from psycopg2.extras import RealDictCursor


def fetch_properties(conn, filters=None):
    filters = filters or {}

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

    budget_max = filters.get("budget_max")

    if budget_max:
        sql += " AND price_vnd_mln <= %s "
        params.append(float(budget_max))

    sql += """
    ORDER BY score DESC NULLS LAST
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()
