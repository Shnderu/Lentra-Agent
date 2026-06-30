from typing import Dict, List


class FeedbackStore:

    def __init__(self):
        self.memory: List[Dict] = []

    def add(self, listing: Dict, action: str):

        """
        action: 'click' | 'save' | 'ignore'
        """

        self.memory.append({
            "listing": listing,
            "action": action
        })

    def get_all(self):
        return self.memory
