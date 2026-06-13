# ============================================================
# SCRAPER NORMALIZER V16.0
# ============================================================

from lentra.rent.models import CanonicalListing
from lentra.rent.normalizers.base import BaseNormalizer


class ScraperNormalizer(BaseNormalizer):
    source_name = "scraper"

    def normalize(self, raw):
        return CanonicalListing(
            id=f"scraper::{raw.get('id')}",
            original_id=raw.get("id"),
            title=raw.get("title"),
            city=raw.get("city"),
            price=float(raw.get("price", 0)),
            rooms=raw.get("rooms"),
            area=None,
            source=self.source_name,
            source_weight=0.9,
        )
