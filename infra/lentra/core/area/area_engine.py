from typing import Dict, Any


class AreaEngine:
    """
    SEA Expansion Prep v1

    PURPOSE:
    - isolate geography intelligence from Market Intelligence core
    - provide city-level scoring for Vietnam

    SUPPORTED CITIES (v1):
    - da_nang
    - nha_trang
    - hanoi
    - ho_chi_minh
    - hoi_an
    - da_lat
    """

    CITY_WEIGHTS = {
        "da_nang": {
            "expat_density": 0.95,
            "tourism": 0.9,
            "cost_index": 0.75
        },
        "nha_trang": {
            "expat_density": 0.85,
            "tourism": 0.95,
            "cost_index": 0.7
        },
        "hanoi": {
            "expat_density": 0.7,
            "tourism": 0.6,
            "cost_index": 0.85
        },
        "ho_chi_minh": {
            "expat_density": 0.9,
            "tourism": 0.7,
            "cost_index": 0.9
        },
        "hoi_an": {
            "expat_density": 0.75,
            "tourism": 0.98,
            "cost_index": 0.65
        },
        "da_lat": {
            "expat_density": 0.6,
            "tourism": 0.8,
            "cost_index": 0.6
        }
    }

    def detect_city(self, query: str) -> str:
        q = query.lower()

        if "da nang" in q:
            return "da_nang"
        if "nha trang" in q:
            return "nha_trang"
        if "hanoi" in q:
            return "hanoi"
        if "ho chi minh" in q or "saigon" in q:
            return "ho_chi_minh"
        if "hoi an" in q:
            return "hoi_an"
        if "da lat" in q or "dalat" in q:
            return "da_lat"

        return "da_nang"  # default MVP city

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = payload.get("query", "")
        city = self.detect_city(query)

        weights = self.CITY_WEIGHTS.get(city, self.CITY_WEIGHTS["da_nang"])

        score = (
            weights["expat_density"] * 0.5 +
            weights["tourism"] * 0.3 +
            weights["cost_index"] * 0.2
        )

        return {
            "score": round(score, 4),
            "city": city,
            "country": "Vietnam",
            "weights": weights,
            "version": "area_v1_vietnam"
        }
