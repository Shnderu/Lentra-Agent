import redis
from collections import defaultdict

"""
Lentra Observable Core v2
Incident Clustering Engine
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


class IncidentCluster:

    def cluster_by_task(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+")
        results = r.xrange(STREAM_RESULTS, "-", "+")

        clusters = defaultdict(int)

        for _, t in tasks:
            ttype = t.get("type", "unknown")
            clusters[f"task:{ttype}"] += 1

        for _, r_ in results:
            status = r_.get("status", "unknown")
            clusters[f"result:{status}"] += 1

        return dict(clusters)


if __name__ == "__main__":
    import json
    print(json.dumps(IncidentCluster().cluster_by_task(), indent=2))
