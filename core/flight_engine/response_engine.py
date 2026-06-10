from typing import List
from core.flight_engine.gateway.dto import FlightOffer


class ResponseEngine:

    def build(self, offers: List[FlightOffer], origin: str, destination: str, date: str):

        if not offers:
            return (
                "❌ Рейсы не найдены\n\n"
                f"{origin} → {destination}\n"
                f"Дата: {date}"
            )

        top = offers[:3]

        lines = []
        lines.append("✈️ Результаты поиска\n")
        lines.append(f"{origin} → {destination}")
        lines.append(f"Дата: {date}\n")

        for i, o in enumerate(top, 1):

            lines.append(
                f"💺 Вариант {i}\n"
                f"💰 Цена: {o.price} {o.currency}\n"
                f"⏱ Время: {o.duration}\n"
                f"✈️ Авиакомпания: {o.airline}\n"
                f"📡 Провайдер: {o.provider}\n"
            )

        best = offers[0]

        lines.append("🏆 Лучший вариант")
        lines.append(f"{best.price} {best.currency} — {best.airline}")

        return "\n".join(lines)
