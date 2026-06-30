class AdaptiveWeights:

    def __init__(self):

        # стартовые веса (OS v1 baseline)
        self.weights = {
            "price": 0.5,
            "expat": 0.3,
            "risk": 0.2
        }

    def update(self, feedback: list):

        """
        very lightweight online adjustment
        """

        for item in feedback:

            action = item["action"]

            if action == "save":
                self.weights["expat"] += 0.01
                self.weights["risk"] -= 0.005

            if action == "ignore":
                self.weights["risk"] += 0.01

        # normalize
        total = sum(self.weights.values())

        for k in self.weights:
            self.weights[k] /= total

        return self.weights
