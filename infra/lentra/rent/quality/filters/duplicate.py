# ============================================================
# DUPLICATE DETECTION V16.3
# ============================================================

import hashlib


def duplicate_score(listing: dict, seen: set) -> float:
    key = hashlib.md5(
        f"{listing.get('title')}_{listing.get('price')}_{listing.get('city')}".encode()
    ).hexdigest()

    if key in seen:
        return 100  # exact duplicate

    seen.add(key)
    return 0
