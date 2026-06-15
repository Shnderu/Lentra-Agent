from typing import List
from lentra.bot.services.registry import SearchResult


class SearchFormatter:
    @staticmethod
    def format(results: List[SearchResult], offset: int = 0, limit: int = 5) -> str:
        if not results:
            return "Ничего не найдено по запросу."

        chunk = results[offset:offset + limit]

        lines = [f"📊 Результаты {offset + 1}-{offset + len(chunk)}:\n"]

        for r in chunk:
            lines.append(
                "🏠 {title}\n"
                "💰 {price} млн VND\n"
                "📍 {city}, {district}\n"
                "⭐ {score}\n"
                "{extra}\n"
                "──────────────"
                .format(
                    title=r.title or "Без названия",
                    price=r.price_vnd_mln or 0,
                    city=r.city or "-",
                    district=r.district or "-",
                    score=r.score or 0,
                    extra=SearchFormatter._extra(r),
                )
            )

        return "\n".join(lines)

    @staticmethod
    def _extra(r: SearchResult) -> str:
        flags = []
        if r.pool:
            flags.append("🏊 pool")
        if r.sea_view:
            flags.append("🌊 sea view")

        return " | ".join(flags) if flags else ""
