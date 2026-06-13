# ============================================================
# LENTRA NORMALIZATION ENGINE V16.0
# ============================================================

from typing import List
from lentra.rent.models import CanonicalListing


class NormalizationEngine:
    def __init__(self, normalizers):
        self.normalizers = normalizers

    def normalize_batch(self, raw_items: List[dict]) -> List[CanonicalListing]:
        normalized = []

        for item in raw_items:
            source = item.get("source")

            normalizer = self._get_normalizer(source)
            if not normalizer:
                continue

            normalized.append(normalizer.normalize(item))

        return normalized

    def _get_normalizer(self, source):
        for n in self.normalizers:
            if n.source_name == source:
                return n
        return None
