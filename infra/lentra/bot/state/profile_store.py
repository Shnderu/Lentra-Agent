import json
import redis

from lentra.bot.state.profile import UserProfile


class ProfileStore:

    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def _key(self, user_id: int):
        return f"profile:{user_id}"

    def load(self, user_id: int) -> UserProfile:

        raw = self.redis.get(self._key(user_id))

        if not raw:
            return UserProfile(user_id=user_id)

        return UserProfile(**json.loads(raw))

    def save(self, profile: UserProfile):

        self.redis.set(
            self._key(profile.user_id),
            json.dumps(profile.__dict__)
        )
