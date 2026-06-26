from typing import Dict, Optional


class GeoClassifier:
    """
    VIETNAM GEO CLASSIFIER (RULE-BASED)

    Output:
    - country
    - region (North / Central / South)
    - city
    - district (optional heuristic pass later)

    IMPORTANT:
    - no external dependencies
    - no ML
    - deterministic mapping only
    """

    REGION_MAP = {
        "North": {
            "hanoi", "hai phong", "bac ninh", "ninh binh", "ha noi"
        },
        "Central": {
            "da nang", "hue", "hoi an", "nha trang"
        },
        "South": {
            "ho chi minh", "ho chi minh city", "hcm", "saigon",
            "can tho", "vung tau", "bien hoa"
        }
    }

    def classify(self, raw_location: str) -> Dict[str, Optional[str]]:
        if not raw_location:
            return self._empty()

        text = raw_location.lower()

        region = self._detect_region(text)
        city = self._detect_city(text)

        return {
            "country": "Vietnam",
            "region": region,
            "city": city,
            "district": None  # reserved for later enrichment layer
        }

    def _detect_region(self, text: str) -> Optional[str]:
        for region, keywords in self.REGION_MAP.items():
            for k in keywords:
                if k in text:
                    return region
        return None

    def _detect_city(self, text: str) -> Optional[str]:
        # explicit city extraction (simple heuristic layer)
        for region_keywords in self.REGION_MAP.values():
            for city in region_keywords:
                if city in text:
                    return city.title()
        return None

    def _empty(self):
        return {
            "country": "Vietnam",
            "region": None,
            "city": None,
            "district": None
        }
