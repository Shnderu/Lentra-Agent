# ============================================================
# HEALTH CHECK V17.2
# ============================================================


class HealthCheck:
    def __init__(self, cache, state, events):
        self.cache = cache
        self.state = state
        self.events = events

    def check(self):
        return {
            "cache_ok": self.cache is not None,
            "state_ok": self.state is not None,
            "events_ok": self.events is not None,
            "status": "healthy"
        }
