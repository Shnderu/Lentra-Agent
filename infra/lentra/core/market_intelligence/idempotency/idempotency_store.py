import time
import hashlib


class IdempotencyStore:

    def __init__(self, ttl_seconds=3600):
        self.store = {}
        self.ttl = ttl_seconds

    def _now(self):
        return time.time()

    def make_key(self, listing: dict) -> str:
        """
        Stable fingerprint across sources
        """

        raw = (
            str(listing.get("title", "")) +
            str(listing.get("price", "")) +
            str(listing.get("location", "")) +
            str(listing.get("area", "")) +
            str(listing.get("source_url", ""))
        )

        return hashlib.sha256(raw.encode()).hexdigest()

    def seen(self, key: str) -> bool:
        self._cleanup()

        return key in self.store

    def mark(self, key: str):
        self.store[key] = self._now()

    def _cleanup(self):
        now = self._now()
        expired = [k for k, v in self.store.items() if now - v > self.ttl]

        for k in expired:
            del self.store[k]
