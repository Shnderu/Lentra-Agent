import redis

"""
Lentra Observable Core v3
Pre-Failure Detector

Detects conditions BEFORE failure appears
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_RESULTS = "stream:rent:results"


class PreFailureDetector:

    def detect(self):
        results = r.xrange(STREAM_RESULTS, "-", "+")

        failures = 0
        total = len(results)

        for _, r_ in results:
            if r_.get("status") != "done":
                failures += 1

        failure_ratio = failures / total if total else 0

        return {
            "failure_ratio": failure_ratio,
            "risk": "HIGH" if failure_ratio > 0.2 else "LOW"
        }


if __name__ == "__main__":
    import json

    d = PreFailureDetector()
    print(json.dumps(d.detect(), indent=2))
