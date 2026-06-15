from lentra.bot.services.registry import SearchResult


class FilterEngine:

    def apply(self, results: list[SearchResult], filters: dict) -> list[SearchResult]:
        filtered = results

        if filters.get("pool"):
            filtered = [r for r in filtered if r.pool]

        if filters.get("sea"):
            filtered = [r for r in filtered if r.sea_view]

        if "price_max" in filters:
            filtered = [
                r for r in filtered
                if r.price_vnd_mln <= filters["price_max"]
            ]

        return filtered
