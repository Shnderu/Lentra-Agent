import json
import redis

from lentra.bot.state.session import SessionState


class StateStore:

    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def _key(self, user_id: int) -> str:
        return f"session:{user_id}"

    def save(self, state: SessionState):
        self.redis.set(
            self._key(state.user_id),
            json.dumps(state.__dict__, default=str)
        )

    def load(self, user_id: int) -> SessionState:
        raw = self.redis.get(self._key(user_id))

        if not raw:
            return SessionState(user_id=user_id)

        return SessionState(**json.loads(raw))
