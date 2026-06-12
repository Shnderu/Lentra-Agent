import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

LEADER_KEY = "cluster:leader"
LEASE_TTL = 10


def try_become_leader(node_id):
    current = r.get(LEADER_KEY)

    if current:
        return current

    ok = r.set(LEADER_KEY, node_id, nx=True, ex=LEASE_TTL)

    if ok:
        return node_id

    return r.get(LEADER_KEY)


def renew_leadership(node_id):
    current = r.get(LEADER_KEY)

    if current == node_id:
        r.expire(LEADER_KEY, LEASE_TTL)
