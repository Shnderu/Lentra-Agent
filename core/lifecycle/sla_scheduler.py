import time


class SLAScheduler:
    """
    Very simple SLA tracking layer.
    """

    def __init__(self, sla_seconds=60):
        self.sla_seconds = sla_seconds

    def is_breached(self, created_at: float) -> bool:
        return (time.time() - created_at) > self.sla_seconds

    def time_left(self, created_at: float) -> float:
        return max(0, self.sla_seconds - (time.time() - created_at))
