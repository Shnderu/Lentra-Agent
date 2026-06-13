from typing import Dict


def render_card(card: Dict) -> str:
    title = card.get("title", "Object")
    price = card.get("price", "—")
    city = card.get("city", "—")
    score = card.get("meta", {}).get("score", 0)

    text = f"""
🏠 {title}

💰 {price}
📍 {city}
⭐ match: {round(score, 2)}
""".strip()

    return text


def render_message(ux):
    screen = ux.get("screen")

    if screen == "property_list":
        cards = ux.get("cards", [])

        text_blocks = []

        for c in cards[:5]:
            text_blocks.append(render_card(c))

        return "\n\n---\n\n".join(text_blocks)

    return "No data"
