import hashlib


class SnapshotEngine:

    def build_search_id(self, query: str, filters: dict | None = None) -> str:
        base = query + str(filters or {})
        return hashlib.md5(base.encode()).hexdigest()
