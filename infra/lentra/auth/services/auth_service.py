# ============================================================
# LENTRA AUTH SERVICE V16.9
# ============================================================

import hashlib
import time


class AuthService:
    def __init__(self):
        self.api_keys = {}

    def create_api_key(self, user_id: str):
        key = hashlib.sha256(f"{user_id}-{time.time()}".encode()).hexdigest()

        self.api_keys[key] = {
            "user_id": user_id,
            "created_at": time.time()
        }

        return key

    def validate(self, api_key: str):
        return self.api_keys.get(api_key)
