import redis

"""
Lentra Observable Core v5
Incident Classifier
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


class IncidentClassifier:

    def classify(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+")
        results = r.xrange(STREAM_RESULTS, "-", "+")

        lag = len(tasks) - len(results)

        if lag == 0:
            severity = "NONE"
        elif lag <= 3:
            severity = "LOW"
        elif lag <= 10:
            severity = "MEDIUM"
        else:
            severity = "HIGH"

        return {
            "lag": lag,
            "severity": severity
        }


if __name__ == "__main__":
    import json
    print(json.dumps(IncidentClassifier().classify(), indent=2))
