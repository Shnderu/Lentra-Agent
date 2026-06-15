from lentra.bot.services.registry import SearchResult


class CardBuilder:

    def list_card(self, r: SearchResult, idx: int) -> str:
        tags = []
        if r.pool:
            tags.append("🏊 бассейн")
        if r.sea_view:
            tags.append("🌊 море")

        return (
            f"🏡 <b>Вариант {idx}</b>\n"
            f"📍 {r.city}, {r.district}\n"
            f"🏠 {r.title}\n"
            f"💰 <b>{r.price_vnd_mln} млн VND</b>\n"
            f"⭐ {r.score:.1f}\n"
            f"{' | '.join(tags) if tags else '—'}\n"
        )

    def detail_card(self, r: SearchResult) -> str:
        score_hint = "🔥 высокий спрос" if r.score > 4.5 else "⭐ стандарт"

        return (
            f"🏡 <b>Детали объекта</b>\n\n"
            f"📍 <b>{r.city}, {r.district}</b>\n"
            f"🏠 {r.title}\n\n"
            f"💰 <b>{r.price_vnd_mln} млн VND</b>\n"
            f"⭐ {r.score:.1f} ({score_hint})\n\n"
            f"{'🏊 бассейн\n' if r.pool else ''}"
            f"{'🌊 вид на море\n' if r.sea_view else ''}"
        )
