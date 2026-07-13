from typing import List
import asyncio

from lentra.application.rent_search.providers.base.provider import RentProvider
from lentra.application.rent_search.contracts.rent_item import RentSearchItem
from lentra.application.rent_search.dto.search_context import SearchContext
from lentra.application.rent_search.services.normalizer import RentNormalizer


class RentAggregator:

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers
        self.normalizer = RentNormalizer()

    def _select_providers(self, context: SearchContext) -> List[RentProvider]:

        selected = []

        for p in self.providers:

            name = p.__class__.__name__.lower()

            # Thailand provider only for thailand
            if "thailand" in name:
                if context.country == "thailand":
                    selected.append(p)
                continue

            # scraper always active (fallback/global)
            if "scraper" in name:
                selected.append(p)
                continue

            # social only if no country constraint
            if "social" in name:
                if not context.country:
                    selected.append(p)
                continue

            # default allow
            selected.append(p)

        return selected

    async def search(self, context: SearchContext) -> List[RentSearchItem]:

        providers = self._select_providers(context)

        tasks = [
            provider.search(context)
            for provider in providers
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        items: List[RentSearchItem] = []

        for r in results:
            if isinstance(r, Exception):
                continue
            items.extend(r)

        # -------------------------
        # NORMALIZATION
        # -------------------------
        normalized: List[RentSearchItem] = []

        for item in items:
            try:
                if context.country:
                    item = self.normalizer.normalize(item, context.country)
                normalized.append(item)
            except Exception:
                normalized.append(item)

        # -------------------------
        # DEDUPLICATION
        # -------------------------
        seen = set()
        deduped: List[RentSearchItem] = []

        for item in normalized:

            key = (
                (item.city or "").strip().lower(),
                (item.title or "").strip().lower()
            )

            if key in seen:
                continue

            seen.add(key)
            deduped.append(item)

        return deduped
