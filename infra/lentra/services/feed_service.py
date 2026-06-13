from lentra.services.ranking_service import get_feed


class FeedService:

    def __init__(self):
        pass

    def get_feed(self, limit=10):
        return get_feed(limit=limit)
