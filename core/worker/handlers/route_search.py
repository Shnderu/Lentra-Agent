from core.flight_engine.service import FlightSearchService


async def handle(task):

    service = FlightSearchService()

    payload = task["payload"]

    result = await service.search(
        payload["origin"],
        payload["destination"],
        payload["date"]
    )

    offers = result.get("offers", [])

    if not offers:
        return "❌ Рейсы не найдены"

    top = offers[:3]

    lines = []
    lines.append("✈️ Результаты поиска\n")
    lines.append(f"{result['origin']} → {result['destination']}")
    lines.append(f"Дата: {result['date']}\n")

    for i, item in enumerate(top, 1):

        offer = item["offer"]

        lines.append(
            f"💺 Вариант {i}\n"
            f"💰 {offer.price} {offer.currency}\n"
            f"⏱ {offer.duration}\n"
            f"✈️ {offer.airline}\n"
            f"📡 {offer.provider}\n"
            f"🧠 Score: {item['score']}\n"
            f"📌 {item['reason']}\n"
            f"⚠️ Risk: {item['risk']}\n"
        )

    best = top[0]

    b = best["offer"]

    lines.append("\n🏆 Лучший вариант")
    lines.append(f"{b.price} {b.currency} — {b.airline}")

    return "\n".join(lines)
