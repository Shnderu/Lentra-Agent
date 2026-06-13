# ============================================================
# FEEDBACK PROCESSOR V16.6
# ============================================================

from collections import defaultdict


class FeedbackProcessor:
    def build_signals(self, events):
        """
        превращает события в сигналы ранжирования
        """

        signals = defaultdict(float)

        for e in events:
            if e.event_type == "click":
                signals[e.listing_id] += 5

            elif e.event_type == "view":
                signals[e.listing_id] += 1

            elif e.event_type == "save":
                signals[e.listing_id] += 10

            elif e.event_type == "ignore":
                signals[e.listing_id] -= 3

        return dict(signals)
