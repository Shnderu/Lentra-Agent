class WeightStore:

    def __init__(self):
        self.weights = {
            "price": 20,
            "location": 15,
            "title": 10,
            "text_match": 30,
            "source": 5
        }

    def update(self, signal: dict):
        """
        Очень простое адаптивное обучение
        """

        if signal["signal"] == "click":
            self.weights["text_match"] += 1
            self.weights["location"] += 0.5

        if signal["signal"] == "skip":
            self.weights["price"] -= 0.5

    def get(self):
        return self.weights
