class FeedbackCollector:

    def collect(self, query: dict, items: list, clicked_index: int = None):
        """
        Простая модель implicit feedback
        """

        return {
            "query": query,
            "clicked_index": clicked_index,
            "impressions": len(items),
            "signal": "click" if clicked_index is not None else "skip"
        }
