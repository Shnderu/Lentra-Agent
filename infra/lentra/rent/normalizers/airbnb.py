# ============================================================
# PATCH V16.1 - GEO NORMALIZATION
# ============================================================

from lentra.rent.models import CanonicalListing
from lentra.rent.normalizers.base import BaseNormalizer


class AirbnbNormalizer(BaseNormalizer):
    source_name = "airbnb"

    def normalize(self, raw):
        return CanonicalListing(
            id=f"airbnb::{raw.get('id')}",
            original_id=raw.get("id"),
            title=raw.get("title"),
            city=raw.get("city"),
            price=float(raw.get("price", 0)),
            rooms=raw.get("rooms"),
            area=None,
            source=self.source_name,
            source_weight=1.2,

            # MOCK GEO (в реальности будет из API/парсинга)
            lat=raw.get("lat"),
            lon=raw.get("lon"),
            district=raw.get("district"),
        )
