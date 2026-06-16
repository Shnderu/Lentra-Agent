import json


class ResultCache:

    def __init__(self, redis):
        self.redis = redis

    def set_results(self, search_id: str, items: list):
        self.redis.set(
            f"results:{search_id}",
            json.dumps([i.__dict__ for i in items])
        )

    def get_results(self, search_id: str):
        raw = self.redis.get(f"results:{search_id}")
        if not raw:
            return []
        return json.loads(raw)
