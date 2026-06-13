# ============================================================
# CACHE KEY BUILDER V16.7
# ============================================================

import hashlib
import json


def build_search_key(query: dict):
    raw = json.dumps(query, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()
