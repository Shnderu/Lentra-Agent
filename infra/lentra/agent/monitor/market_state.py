# ============================================================
# MARKET STATE TRACKER V17.1
# ============================================================


class MarketState:
    def __init__(self):
        self.last_seen = {}

    def update(self, listing):
        self.last_seen[listing["id"]] = listing

    def get_previous(self, listing_id):
        return self.last_seen.get(listing_id)
