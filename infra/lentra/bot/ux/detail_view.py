from lentra.bot.services.registry import SearchResult


class DetailView:

    def render(self, r: SearchResult, item_id: int) -> str:
        tags = []

        if r.pool:
            tags.append("🏊 бассейн")
        if r.sea_view:
            tags.append("🌊 вид на море")

        return (
            f"🏡 <b>Объект #{item_id}</b>\n\n"
            f"📍 <b>{r.city}, {r.district}</b>\n"
            f"🏠 {r.title}\n\n"
            f"💰 <b>{r.price_vnd_mln} млн VND</b>\n"
            f"⭐ рейтинг: {r.score:.1f}\n\n"
            f"{' | '.join(tags) if tags else '—'}\n\n"
            f"📦 Детальная информация загружается...\n"
            f"🧭 карта / фото / контакты (следующий шаг)"
        )
