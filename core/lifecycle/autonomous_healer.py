import time


class AutonomousHealer:
    """
    Simple self-healing controller (reactive rules only for now).
    """

    def should_restart_worker(self, failure_rate: float) -> bool:
        return failure_rate > 0.6

    def backoff_time(self, consecutive_failures: int) -> int:
        return min(60, 2 ** consecutive_failures)
