from lentra.core.market_intelligence.learning.feedback_store import FeedbackStore
from lentra.core.market_intelligence.learning.adaptive_weights import AdaptiveWeights


class EvolutionEngine:

    def __init__(self):

        self.store = FeedbackStore()
        self.weights = AdaptiveWeights()

    def record_feedback(self, listing, action):

        self.store.add(listing, action)

    def update_model(self):

        feedback = self.store.get_all()

        return self.weights.update(feedback)

    def get_weights(self):
        return self.weights.weights
