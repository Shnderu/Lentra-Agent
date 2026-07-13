import re
from typing import Dict, Any, Optional

from lentra.core.data_layer.geo.classifier import GeoClassifier


class NormalizationEngine:
    """
    DATA NORMALIZATION LAYER (VIETNAM ONLY VND)

    RULE:
    - all canonical prices stored ONLY in VND
    - source currency is preserved
    - no FX layer in system
    """

    def __init__(self):
        self.geo = GeoClassifier()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": raw.get("id"),
            "source": raw.get("source"),
            "source_url": raw.get("source_url"),

            "title": self._clean_text(raw.get("title")),
            "description": self._clean_text(raw.get("description")),

            # Canonical internal price format
            "price_vnd": self._normalize_price_vnd(
                raw.get("price"),
                raw.get("currency")
            ),

            # Preserve source information
            "price_original": raw.get("price"),
            "currency_original": raw.get("currency"),

            "property_type": self._normalize_property_type(
                raw.get("property_type")
            ),

            "size_m2": self._parse_float(
                raw.get("size")
            ),

            "rooms": self._parse_int(
                raw.get("rooms")
            ),

            "location": self.geo.classify(
                raw.get("location")
            ),

            "images": raw.get("images") or [],
            "contact": raw.get("contact"),
            "timestamp": raw.get("timestamp"),
        }

    # -------------------------
    # PRICE NORMALIZATION
    # -------------------------

    def _normalize_price_vnd(
        self,
        price: Any,
        currency: Optional[str] = None
    ) -> Optional[int]:

        if price is None:
            return None

        try:
            value = float(
                str(price)
                .replace(",", "")
                .strip()
            )

            currency = (
                currency or "VND"
            ).upper()

            if currency == "USD":
                value *= 26000

            return int(value)

        except Exception:
            return None

    # -------------------------
    # TEXT CLEANING
    # -------------------------

    def _clean_text(
        self,
        text: Optional[str]
    ) -> Optional[str]:

        if not text:
            return None

        return re.sub(
            r"\s+",
            " ",
            text
        ).strip()

    # -------------------------
    # PROPERTY TYPE
    # -------------------------

    def _normalize_property_type(
        self,
        value: Optional[str]
    ) -> Optional[str]:

        if not value:
            return None

        v = value.lower()

        if "studio" in v:
            return "studio"

        if "apartment" in v or "flat" in v:
            return "apartment"

        if "villa" in v:
            return "villa"

        if "room" in v:
            return "room"

        return "unknown"

    # -------------------------
    # NUMERIC PARSING
    # -------------------------

    def _parse_float(
        self,
        value: Any
    ) -> Optional[float]:

        if value is None:
            return None

        try:
            return float(
                str(value)
                .replace(",", "")
                .strip()
            )

        except Exception:
            return None

    def _parse_int(
        self,
        value: Any
    ) -> Optional[int]:

        if value is None:
            return None

        try:
            return int(
                float(
                    str(value).strip()
                )
            )

        except Exception:
            return None
