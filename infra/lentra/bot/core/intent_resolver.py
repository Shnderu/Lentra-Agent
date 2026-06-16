from lentra.bot.core.intent import Intent


class IntentResolver:

    def resolve(self, text: str) -> Intent:

        if not text:
            return Intent.UNKNOWN

        t = text.lower().strip()

        # SEARCH
        if any(x in t for x in ["найти", "поиск", "rent", "apartment", "rent"]):
            return Intent.SEARCH

        # FILTER
        if any(x in t for x in ["фильтр", "filter", "бюджет", "район"]):
            return Intent.FILTER

        # BACK
        if t in ["назад", "back", "⬅️"]:
            return Intent.BACK

        return Intent.SEARCH
