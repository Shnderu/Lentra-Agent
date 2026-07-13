from lentra.bot.state.state_store import StateStore


class Registry:
    """
    Legacy runtime registry.

    Search services moved to application container.
    This object only keeps bot runtime state.
    """

    def __init__(self):
        self.state_store = StateStore()
