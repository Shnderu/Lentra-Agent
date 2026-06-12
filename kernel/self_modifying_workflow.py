import redis
import os
import json

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)


def load_workflow(wf_id):
    return r.get(f"wf:{wf_id}")


def mutate_workflow(wf_id, signal):
    wf = load_workflow(wf_id)

    if not wf:
        return None

    wf = json.loads(wf)

    if signal == "scale_architecture":
        wf["nodes"].append("autoscaler")

    if signal == "mutate_fallback_strategy":
        wf["nodes"].insert(0, "failover_guard")

    r.set(f"wf:{wf_id}", json.dumps(wf))

    return wf
