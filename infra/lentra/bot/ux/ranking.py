from lentra.bot.services.registry import SearchResult


class RankingEngine:

    def rank(self, results: list[SearchResult]) -> list[SearchResult]:
        return sorted(
            results,
            key=lambda r: (
                r.score * 2 +
                (1 if r.pool else 0) +
                (1 if r.sea_view else 0)
            ),
            reverse=True
        )
