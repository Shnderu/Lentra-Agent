from collections import defaultdict


class FeedbackStore:

    def __init__(self):

        self.impressions = defaultdict(int)
        self.clicks = defaultdict(int)

    def log_impression(self, key: str):
        self.impressions[key] += 1

    def log_click(self, key: str):
        self.clicks[key] += 1

    def get_click_rate(self, key: str) -> float:

        imp = self.impressions[key]
        clk = self.clicks[key]

        if imp == 0:
            return 0.0

        return clk / imp
