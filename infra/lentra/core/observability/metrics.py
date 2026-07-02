from collections import defaultdict


class Metrics:
    """
    LIGHTWEIGHT IN-MEMORY METRICS (NO EXTERNAL DEPENDENCIES)
    """

    def __init__(self):
        self.engine_calls = defaultdict(int)
        self.engine_errors = defaultdict(int)

    def inc_call(self, engine: str):
        self.engine_calls[engine] += 1

    def inc_error(self, engine: str):
        self.engine_errors[engine] += 1

    def snapshot(self):
        return {
            "calls": dict(self.engine_calls),
            "errors": dict(self.engine_errors)
        }


metrics = Metrics()
