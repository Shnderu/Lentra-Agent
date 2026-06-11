import redis
import time
import json


class AtomicQueueV2:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def push(self, stream: str, idem_key: str, task_id: str, payload: dict) -> bool:
        lua = """
        -- idempotency check
        if redis.call('EXISTS', KEYS[1]) == 1 then
            return 0
        end

        -- mark idempotent first (safe write)
        redis.call('SET', KEYS[1], ARGV[1], 'EX', ARGV[4])

        local ok = redis.call('XADD', KEYS[2], '*',
            'task_id', ARGV[2],
            'payload', ARGV[3],
            'created_at', ARGV[5]
        )

        -- rollback idempotency key if stream failed
        if not ok then
            redis.call('DEL', KEYS[1])
            return 0
        end

        return 1
        """

        return bool(
            self.r.eval(
                lua,
                2,
                idem_key,
                stream,
                "1",
                task_id,
                json.dumps(payload),
                str(int(time.time())),
                3600
            )
        )
