from lentra.services.ranking_service import RankingService

service = RankingService()

feed = service.get_feed(limit=10)

for item in feed:
    print(
        f"[{item['confidence']}] "
        f"{item['price']} {item['currency']} | "
        f"{item['location']} | "
        f"{item['type']}\n"
        f"{item['description'][:80]}"
    )
    print("-" * 50)
