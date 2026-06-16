from typing import Dict


class Renderer:
    def render_card(self, card: Dict) -> str:
        title = card.get("title", "Object")
        price = card.get("price", "—")
        city = card.get("city", "—")
        score = card.get("meta", {}).get("score", 0)

        return (
            f"🏠 {title}\n\n"
            f"💰 {price}\n"
            f"📍 {city}\n"
            f"⭐ match: {round(score, 2)}"
        )

    def render_message(self, ux: Dict) -> str:
        screen = ux.get("screen")

        if screen == "property_list":
            cards = ux.get("cards", [])
            return "\n\n---\n\n".join(
                self.render_card(c) for c in cards[:5]
            )

        return "No data"


# публичный singleton (UI слой самодостаточный)
renderer = Renderer()
