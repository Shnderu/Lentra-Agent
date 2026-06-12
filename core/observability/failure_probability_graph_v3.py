import redis
from collections import defaultdict, Counter

"""
Lentra Observable Core v3
Failure Probability Graph

Детерминированная модель предсказания отказов
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


class FailureProbabilityGraph:

    def build_transition_matrix(self):
        events = r.xrange(STREAM_EVENTS, "-", "+")

        transitions = defaultdict(list)
        last_type = None

        for _, e in events:
            etype = e.get("type")

            if last_type:
                transitions[last_type].append(etype)

            last_type = etype

        return transitions

    def compute_risk(self):
        transitions = self.build_transition_matrix()

        risk = {}

        for source, targets in transitions.items():
            total = len(targets)
            counter = Counter(targets)

            risk[source] = {
                "total_transitions": total,
                "entropy": len(counter),
                "dominant_next": counter.most_common(1)[0] if counter else None,
                "failure_risk_score": len(counter) / (total + 1)
            }

        return risk


if __name__ == "__main__":
    import json
    g = FailureProbabilityGraph()
    print(json.dumps(g.compute_risk(), indent=2))
