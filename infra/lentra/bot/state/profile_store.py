import json
import os

from lentra.bot.state.profile import UserProfile


class ProfileStore:

    def __init__(self, path="/tmp/lentra_profiles"):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def _file(self, user_id: int):
        return f"{self.path}/{user_id}.json"

    def load(self, user_id: int) -> UserProfile:
        file = self._file(user_id)

        if not os.path.exists(file):
            return UserProfile(user_id=user_id)

        with open(file, "r") as f:
            data = json.load(f)

        return UserProfile(**data)

    def save(self, profile: UserProfile):

        with open(self._file(profile.user_id), "w") as f:
            json.dump(profile.__dict__, f)
