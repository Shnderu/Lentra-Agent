from sqlalchemy import text

def fetch_properties(db, query_obj):
    sql = text("""
        SELECT id, title, price_vnd_mln, area_m2, city, district, pool, sea_view, score
        FROM properties
        WHERE city = :city
        LIMIT 50
    """)

    result = db.execute(sql, {
        "city": query_obj.get("city", "Da Nang")
    })

    rows = result.mappings().all()

    return rows
