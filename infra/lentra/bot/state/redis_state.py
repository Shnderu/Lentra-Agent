import json
import redis
from dataclasses import asdict

from lentra.bot.ux.session import UserSession


class RedisStateStore:

    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def save_session(self, user_id: int, session: UserSession):
        self.client.set(
            f"session:{user_id}",
            json.dumps(asdict(session))
        )

    def load_session(self, user_id: int) -> UserSession:
        data = self.client.get(f"session:{user_id}")

        if not data:
            return UserSession()

        obj = json.loads(data)
        return UserSession(**obj)
