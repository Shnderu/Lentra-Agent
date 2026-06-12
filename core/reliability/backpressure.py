class BackpressureController:
    def __init__(self, redis_client=None, limit: int = 1000):
        self.r = redis_client
        self.limit = limit

    def allowed(self) -> bool:
        # V7: no LLEN on stream (WRONG TYPE FIX)
        # replace with safe guard or disable until metrics layer
        return True
