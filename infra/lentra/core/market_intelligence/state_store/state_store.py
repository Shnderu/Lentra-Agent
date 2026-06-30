from collections import defaultdict
import time


class StateStore:
    """
    Live market snapshot storage (in-memory MVP)
    """

    def __init__(self):
        self.state = defaultdict(dict)

    def update_listing(self, listing: dict):
        key = f"{listing.get('location', {}).get('segment','unknown')}"

        self.state[key] = {
            "last_price": listing.get("price"),
            "market_price": listing.get("market_price"),
            "risk": listing.get("risk"),
            "timestamp": time.time()
        }

    def get_state(self, segment: str):
        return self.state.get(segment, {})
