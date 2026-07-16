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


    def normalize(
        self,
        raw: Dict[str, Any]
    ) -> Dict[str, Any]:

        location_raw = raw.get(
            "location"
        )

        geo_parts = []


        if isinstance(location_raw, dict):

            geo_parts.extend(
                [
                    str(location_raw.get("city") or ""),
                    str(location_raw.get("district") or "")
                ]
            )

        elif location_raw:

            geo_parts.append(
                str(location_raw)
            )


        geo_parts.extend(
            [
                str(raw.get("city") or ""),
                str(raw.get("district") or ""),
                str(raw.get("title") or ""),
                str(raw.get("description") or ""),
            ]
        )


        location_raw = " ".join(
            [
                part
                for part in geo_parts
                if part
            ]
        )


        location = self.geo.classify(
            location_raw
        )


        property_type = self._normalize_property_type(
            raw.get("property_type"),
            raw.get("title"),
            raw.get("description")
        )


        return {

            "id": raw.get("id"),

            "source": raw.get("source"),

            "source_url": raw.get("source_url"),

            "title": self._clean_text(
                raw.get("title")
            ),

            "description": self._clean_text(
                raw.get("description")
            ),

            "price_vnd": self._normalize_price_vnd(
                raw.get("price_vnd")
                if raw.get("price_vnd") is not None
                else raw.get("price"),
                raw.get("currency")
            ),

            "price_original": (
                raw.get("price_vnd")
                if raw.get("price_vnd") is not None
                else raw.get("price")
            ),

            "currency_original": (
                raw.get("currency")
                or "VND"
            ),

            "property_type": property_type,

            "size_m2": self._parse_float(
                raw.get("size")
            ),

            "rooms": self._parse_int(
                raw.get("rooms")
            ),

            "location": location,

            "city": location.get(
                "city"
            ),

            "district": location.get(
                "district"
            ),

            "segment_key": self._build_segment_key(
                location,
                property_type
            ),

            "images": raw.get("images") or [],

            "contact": raw.get("contact"),

            "timestamp": raw.get("timestamp"),
        }


    def _build_segment_key(
        self,
        location: Dict[str, Any],
        property_type: Optional[str]
    ) -> str:

        city = (
            location.get("city")
            or "unknown"
        ).lower().replace(
            " ",
            "_"
        )

        district = (
            location.get("district")
            or "unknown"
        ).lower().replace(
            " ",
            "_"
        )

        prop = (
            property_type
            or "unknown"
        )

        return (
            f"{city}:{district}:{prop}"
        )


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

            return int(
                value
            )

        except Exception:

            return None


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


    def _normalize_property_type(
        self,
        value: Optional[str],
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> str:

        text = " ".join(
            [
                str(value or ""),
                str(title or ""),
                str(description or "")
            ]
        ).lower()


        if "studio" in text:

            return "studio"


        if (
            "apartment" in text
            or "flat" in text
            or "condo" in text
        ):

            return "apartment"


        if "villa" in text:

            return "villa"


        if "room" in text:

            return "room"


        return "unknown"


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
