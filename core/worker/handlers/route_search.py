from core.flight_engine.service import FlightSearchService


async def handle(task):

    service = FlightSearchService()

    payload = task["payload"]

    result = await service.search(
        payload["origin"],
        payload["destination"],
        payload["date"]
    )

    if not isinstance(result, dict):
        return str(result)

    offers = result.get("offers", [])

    if not offers:
        return "❌ Рейсы не найдены"

    top = offers[:3]

    lines = []
    lines.append("✈️ Результаты поиска\n")
    lines.append(f"{result['origin']} → {result['destination']}")
    lines.append(f"Дата: {result['date']}\n")

    for i, o in enumerate(top, 1):
        lines.append(
            f"💺 Вариант {i}\n"
            f"💰 {o.price} {o.currency}\n"
            f"⏱ {o.duration}\n"
            f"✈️ {o.airline}\n"
            f"📡 {o.provider}\n"
        )

    best = top[0]
    lines.append("\n🏆 Лучший вариант")
    lines.append(f"{best.price} {best.currency} — {best.airline}")

    return "\n".join(lines)
