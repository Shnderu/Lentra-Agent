from collections import defaultdict


class Cache:
    def __init__(self):
        self._store = {}


class ResultCache:
    """
    Совместимый кэш результатов поиска.

    Поддерживает:
    - set_results (используется SearchPipeline)
    - get_results (на будущее)
    """

    def __init__(self, redis=None):
        self.redis = redis
        self._local = defaultdict(dict)

    def set_results(self, search_id: str, items):
        """
        FIX: метод отсутствовал, из-за этого падал pipeline
        """
        self._local[search_id] = {
            "items": items
        }

        return True

    def get_results(self, search_id: str):
        return self._local.get(search_id)
