import redis

"""
Lentra Observable Core v4
Incident Narrative Builder
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


class NarrativeBuilder:

    def build(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+")
        results = r.xrange(STREAM_RESULTS, "-", "+")

        narrative = []

        narrative.append("INCIDENT NARRATIVE")
        narrative.append("==================")

        narrative.append(f"Tasks observed: {len(tasks)}")
        narrative.append(f"Results observed: {len(results)}")

        lag = len(tasks) - len(results)

        if lag > 0:
            narrative.append(f"System lag detected: {lag} unprocessed tasks")
        else:
            narrative.append("No system lag detected")

        # simple interpretation layer
        if lag > 10:
            narrative.append("Conclusion: Worker saturation or queue backpressure likely")
        elif lag > 0:
            narrative.append("Conclusion: Minor processing delay in worker pipeline")
        else:
            narrative.append("Conclusion: System operating normally")

        return {
            "narrative": "\n".join(narrative),
            "lag": lag
        }


if __name__ == "__main__":
    import json
    print(json.dumps(NarrativeBuilder().build(), indent=2))
