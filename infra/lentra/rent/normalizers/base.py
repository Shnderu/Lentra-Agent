# ============================================================
# LENTRA SOURCE NORMALIZER BASE V16.0
# ============================================================

from typing import Dict, Any
from lentra.rent.models import CanonicalListing


class BaseNormalizer:
    source_name: str

    def normalize(self, raw: Dict[str, Any]) -> CanonicalListing:
        raise NotImplementedError
