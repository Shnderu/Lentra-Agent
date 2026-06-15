from sqlalchemy import text


def fetch_properties(conn, query: dict):
    """
    conn = SQLAlchemy Session (из get_db)
    """

    sql = """
        SELECT id, title, price, pool, sea_view
        FROM properties
        LIMIT 50
    """

    result = conn.execute(text(sql), {})
    rows = result.mappings().all()

    return [dict(r) for r in rows]
