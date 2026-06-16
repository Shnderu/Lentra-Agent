class QueryRewriter:

    def rewrite(self, query: str, filters: dict) -> str:

        parts = [query]

        if filters.get("city"):
            parts.append(f'in {filters["city"]}')

        if filters.get("district"):
            parts.append(f'district {filters["district"]}')

        if filters.get("price_min") or filters.get("price_max"):
            parts.append(
                f'price {filters.get("price_min","0")}-{filters.get("price_max","∞")}'
            )

        return " ".join(parts)
