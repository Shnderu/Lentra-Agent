class RankingService:

    def rank(self, results: list[dict]) -> list[dict]:
        """
        Сортировка по "выгодности"
        """

        def score(f):
            return (
                f["price"] * 1.0 +
                f["duration"] * 5.0
            )

        return sorted(results, key=score)


ranking_service = RankingService()
