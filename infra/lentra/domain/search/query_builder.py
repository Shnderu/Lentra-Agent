from typing import Dict, Any, Tuple, List


class QueryBuilder:
    """
    Строит SQL WHERE + параметры из API запроса.
    Это единый слой фильтрации (вместо размазанной логики в SQL и Python).
    """

    def build(self, query: Dict[str, Any]) -> Tuple[str, List[Any]]:
        where = []
        params = []

        # CITY FILTER
        city = query.get("city")
        if city:
            where.append("LOWER(city) = LOWER(%s)")
            params.append(city)

        # BUDGET FILTER
        budget_max = query.get("budget_max")
        if budget_max is not None:
            where.append("price_vnd_mln <= %s")
            params.append(budget_max)

        # OPTIONAL FEATURES FILTERS
        if query.get("pet_friendly") is True:
            where.append("pet_friendly = TRUE")

        if query.get("pool") is True:
            where.append("pool = TRUE")

        if query.get("sea_view") is True:
            where.append("sea_view = TRUE")

        # BASE SQL
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
        """

        if where:
            sql += " WHERE " + " AND ".join(where)

        return sql, params
