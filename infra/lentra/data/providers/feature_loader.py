from lentra.core.feature_store import feature_store


def load_features_from_properties(properties: list):
    """
    Простейшая инициализация feature store из БД результатов.
    """

    for p in properties:
        feature_store.set(p["id"], {
            "sea_view": p.get("sea_view", False),
            "pool": p.get("pool", False),
            "pet_friendly": p.get("pet_friendly", False),
            "area_m2": p.get("area_m2", 0),
            "price": p.get("price_vnd_mln", 0),
        })
