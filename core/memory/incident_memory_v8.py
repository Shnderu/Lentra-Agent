import redis
import hashlib
import json
import time

"""
Lentra Incident Memory v8
Temporal Incident Storage + Matching
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

MEMORY_STREAM = "stream:incident:memory"


class IncidentMemory:

    def store(self, incident: dict):
        fingerprint = self._fingerprint(incident)

        payload = {
            "ts": time.time(),
            "fingerprint": fingerprint,
            "severity": incident.get("severity", "UNKNOWN"),
            "graph_size": incident.get("graph_size", 0),
            "edges": incident.get("edges", 0)
        }

        r.xadd(MEMORY_STREAM, payload)

        return payload

    def search_similar(self, incident: dict):
        fp = self._fingerprint(incident)

        history = r.xrange(MEMORY_STREAM, "-", "+")

        matches = []

        for _, item in history:
            if item.get("fingerprint") == fp:
                matches.append(item)

        return {
            "query_fingerprint": fp,
            "matches": matches,
            "match_count": len(matches)
        }

    def _fingerprint(self, incident: dict):
        raw = json.dumps({
            "severity": incident.get("severity"),
            "graph_size": incident.get("graph_size"),
            "edges": incident.get("edges")
        }, sort_keys=True)

        return hashlib.sha256(raw.encode()).hexdigest()


if __name__ == "__main__":
    mem = IncidentMemory()

    test = {
        "severity": "LOW",
        "graph_size": 5,
        "edges": 4
    }

    stored = mem.store(test)
    print("STORED:", stored)

    print(mem.search_similar(test))
