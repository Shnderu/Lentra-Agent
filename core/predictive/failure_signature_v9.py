"""
Lentra Failure Signature v9
Pre-failure pattern detection
"""


class FailureSignature:

    def detect(self, metrics: dict):

        signals = []

        if metrics.get("queue_lag", 0) > 5:
            signals.append("QUEUE_LAG")

        if metrics.get("error_rate", 0) > 0.2:
            signals.append("HIGH_ERROR_RATE")

        if metrics.get("retry_rate", 0) > 0.3:
            signals.append("RETRY_STORM")

        if metrics.get("memory_spike", False):
            signals.append("MEMORY_PRESSURE")

        return {
            "signals": signals,
            "pre_failure": len(signals) >= 2
        }


if __name__ == "__main__":
    f = FailureSignature()

    print(f.detect({
        "queue_lag": 7,
        "error_rate": 0.25,
        "retry_rate": 0.1,
        "memory_spike": True
    }))
