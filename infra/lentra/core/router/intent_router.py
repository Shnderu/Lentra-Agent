class IntentRouter:
    """
    PURE GRAPH NODE (SYNC ONLY)
    """

    def route(self, event: dict):
        # MUST NOT BE ASYNC
        return {
            "intent": "default",
            "payload": event
        }
