def format_property_response(ranked_items: list):
    if not ranked_items:
        return "Ничего не найдено по вашему запросу."

    top = ranked_items[:5]

    lines = []
    lines.append("🏠 Лучшие варианты по вашему запросу:\n")

    for i, item in enumerate(top, 1):
        lines.append(
            f"{i}. {item.get('title')}\n"
            f"   💰 {item.get('price')} USD\n"
            f"   📍 {item.get('district')}\n"
            f"   ⭐ score: {item.get('score')}\n"
        )

    lines.append("\n👉 Хотите сузить поиск или изменить бюджет?")

    return "\n".join(lines)
