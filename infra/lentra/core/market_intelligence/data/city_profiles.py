from typing import Dict, Any


CITY_PROFILES: Dict[str, Dict[str, Any]] = {
    "da_nang": {
        "name": "Da Nang",
        "areas": {
            "beach": {
                "studio": {
                    "avg_price": 650,
                    "min_price": 500,
                    "max_price": 850,
                },
                "1br": {
                    "avg_price": 750,
                    "min_price": 600,
                    "max_price": 1000,
                },
            }
        },
    },
    "nha_trang": {
        "name": "Nha Trang",
        "areas": {
            "beach": {
                "studio": {
                    "avg_price": 450,
                    "min_price": 350,
                    "max_price": 600,
                },
                "1br": {
                    "avg_price": 550,
                    "min_price": 450,
                    "max_price": 750,
                },
            }
        },
    },
}


def get_city_profile(city: str) -> Dict[str, Any]:
    return CITY_PROFILES.get(city, {})


def get_market_price(
    city: str,
    property_type: str = "studio",
    area: str = "beach",
) -> float:
    profile = get_city_profile(city)

    return (
        profile
        .get("areas", {})
        .get(area, {})
        .get(property_type, {})
        .get("avg_price", 0)
    )
