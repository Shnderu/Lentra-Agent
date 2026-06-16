from lentra.bot.domain.item import Item


class ItemMapper:

    @staticmethod
    def from_api(data: list[dict]) -> list[Item]:

        return [
            Item(
                id=r["id"],
                title=r["title"],
                city=r["city"],
                district=r["district"],
                price_vnd_mln=r["price_vnd_mln"],
                score=r["score"]
            )
            for r in data
        ]

    @staticmethod
    def to_dict(items: list[Item]) -> list[dict]:

        return [item.__dict__ for item in items]
