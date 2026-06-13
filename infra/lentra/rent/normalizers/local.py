# ============================================================
# LOCAL NORMALIZER V16.0
# ============================================================

from lentra.rent.models import CanonicalListing
from lentra.rent.normalizers.base import BaseNormalizer


class LocalNormalizer(BaseNormalizer):
    source_name = "local_board"

    def normalize(self, raw):
        return CanonicalListing(
            id=f"local::{raw.get('id')}",
            original_id=raw.get("id"),
            title=raw.get("title"),
            city=raw.get("city"),
            price=float(raw.get("price", 0)),
            rooms=raw.get("rooms"),
            area=raw.get("area"),
            source=self.source_name,
            source_weight=1.0,
        )
