import hashlib
import json


def _safe_get(obj, key, default=None):
    """
    Универсальный доступ:
    - dict -> .get()
    - object -> getattr()
    """
    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def build_idempotency_key(raw_listing) -> str:
    """
    Генерация стабильного ключа идемпотентности.
    Работает и с dict, и с DTO.
    """

    base = {
        "id": _safe_get(raw_listing, "id"),
        "title": _safe_get(raw_listing, "title"),
        "price": _safe_get(raw_listing, "price"),
        "city": _safe_get(raw_listing, "city"),
        "location": _safe_get(raw_listing, "location"),
        "source": _safe_get(raw_listing, "source"),
    }

    canonical = json.dumps(base, sort_keys=True, ensure_ascii=False)

    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
