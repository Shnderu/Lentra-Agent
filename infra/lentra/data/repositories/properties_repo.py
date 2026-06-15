from sqlalchemy import text


class PropertiesRepository:
    def __init__(self, db):
        self.db = db

    def search_properties(self, city=None, budget_max=None, pool=None, sea_view=None):
        sql = """
        SELECT id, title, price_vnd_mln, area_m2, city, district,
               pool, sea_view
        FROM properties
        WHERE 1=1
        """

        params = {}

        if city:
            sql += " AND city = :city"
            params["city"] = city

        if budget_max is not None:
            sql += " AND price_vnd_mln <= :budget_max"
            params["budget_max"] = budget_max

        if pool is not None:
            sql += " AND pool = :pool"
            params["pool"] = pool

        if sea_view is not None:
            sql += " AND sea_view = :sea_view"
            params["sea_view"] = sea_view

        result = self.db.execute(text(sql), params)
        return [dict(row._mapping) for row in result.fetchall()]
