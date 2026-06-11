import redis
import time


class AtomicQueue:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def push_task(self, stream: str, idem_key: str, task_id: str, payload: dict) -> bool:
        lua = """
        if redis.call('EXISTS', KEYS[1]) == 1 then
            return 0
        end

        redis.call('SET', KEYS[1], '1', 'EX', ARGV[1])
        redis.call('XADD', KEYS[2], '*',
            'task_id', ARGV[2],
            'payload', ARGV[3],
            'created_at', ARGV[4]
        )
        return 1
        """

        return bool(
            self.r.eval(
                lua,
                2,
                idem_key,
                stream,
                3600,
                task_id,
                str(payload),
                str(time.time())
            )
        )
