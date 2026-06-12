import redis

"""
Lentra Observable Core v4
Health Story Generator
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


def health_story():
    tasks = r.xrange(STREAM_TASKS, "-", "+")
    results = r.xrange(STREAM_RESULTS, "-", "+")

    lag = len(tasks) - len(results)

    story = []

    story.append("SYSTEM HEALTH STORY")
    story.append("-------------------")

    if lag == 0:
        story.append("System is fully synchronized.")
        story.append("No backlog detected in processing pipeline.")
    elif lag <= 5:
        story.append("Minor backlog observed in processing queue.")
        story.append("Worker is slightly behind incoming task rate.")
    else:
        story.append("Significant backlog detected.")
        story.append("Processing pipeline is under stress or saturated.")

    return {
        "story": "\n".join(story),
        "lag": lag
    }


if __name__ == "__main__":
    import json
    print(json.dumps(health_story(), indent=2))
