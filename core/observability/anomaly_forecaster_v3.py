import redis
from collections import defaultdict

"""
Lentra Observable Core v3
Anomaly Forecaster

Detects "pre-failure conditions"
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


class AnomalyForecaster:

    def forecast_lag_risk(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+")
        results = r.xrange(STREAM_RESULTS, "-", "+")

        lag = len(tasks) - len(results)

        risk = {
            "lag": lag,
            "risk_level": "LOW"
        }

        if lag > 10:
            risk["risk_level"] = "HIGH"
        elif lag > 5:
            risk["risk_level"] = "MEDIUM"

        return risk


    def detect_hotspot(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+")

        city_counter = defaultdict(int)

        for _, t in tasks:
            payload = t.get("payload", "{}")
            if "Phu Quoc" in payload:
                city_counter["Phu Quoc"] += 1

        return {
            "hotspot": dict(city_counter)
        }


if __name__ == "__main__":
    import json

    f = AnomalyForecaster()

    print(json.dumps({
        "lag_risk": f.forecast_lag_risk(),
        "hotspots": f.detect_hotspot()
    }, indent=2))
