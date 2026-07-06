class TelegramAIBridge:
    """
    Single entrypoint between bot runtime and AI control layer.
    """

    def __init__(self):
        pass

    async def handle_message(self, user_id: int, text: str):
        """
        AI decision layer stub.

        Later will connect:
        - price intelligence
        - risk scoring
        - dedup engine
        """

        # TEMP LOGIC (safe fallback)
        if not text:
            return {
                "override": False
            }

        # basic routing heuristic
        if "price" in text.lower():
            return {
                "override": True,
                "response": "AI: price module not fully connected yet",
                "state_patch": {}
            }

        return {
            "override": False
        }
