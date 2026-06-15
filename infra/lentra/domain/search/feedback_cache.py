from collections import defaultdict


class FeedbackCache:
    def __init__(self):
        self.data = defaultdict(lambda: {"view": 0, "click": 0, "like": 0})

    def add(self, property_id, event_type):
        self.data[property_id][event_type] += 1

    def get(self):
        return self.data
