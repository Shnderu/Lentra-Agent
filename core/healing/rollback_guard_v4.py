import time
import redis

"""
Lentra Stability Layer v4
ROLLBACK GUARD (SAFE STOP SYSTEM)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_POLICIES = "stream:system:policies"
STREAM_ROLLBACK = "stream:system:rollback"


class RollbackGuardV4:

    def run(self):
        print(">>> ROLLBACK GUARD V4 STARTED")

        last_id = "0"

        while True:
            resp = r.xread({STREAM_POLICIES: last_id}, block=5000, count=10)

            if not resp:
                continue

            for _, messages in resp:
                for msg_id, msg in messages:
                    last_id = msg_id

                    policy = msg.get("policy", {})

                    # SAFE RULE: NEVER AUTO APPLY
                    if policy.get("action") == "RETRY_TASK":
                        decision = {
                            "action": "DEFERRED_RETRY",
                            "reason": "safe_mode_v4",
                            "ts": time.time()
                        }
                    else:
                        decision = {
                            "action": "IGNORE",
                            "reason": "safe_mode_v4",
                            "ts": time.time()
                        }

                    print(">>> ROLLBACK DECISION:", decision)

                    r.xadd(STREAM_ROLLBACK, decision)


if __name__ == "__main__":
    RollbackGuardV4().run()
