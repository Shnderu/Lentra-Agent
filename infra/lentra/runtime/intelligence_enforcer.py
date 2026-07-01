from lentra.runtime.intelligence_gateway import interpret


class IntelligenceEnforcer:
    """
    Единственный допустимый способ доступа к AI OS.
    Все остальные вызовы считаются нарушением архитектуры.
    """

    def __init__(self):
        self._blocked_paths = [
            "lentra.core.market_intelligence",
            "lentra.services.intelligence",
            "lentra.api.services",
            "lentra.bot.services"
        ]

    def run(self, payload: dict) -> dict:
        return interpret(payload)


# global singleton
enforcer = IntelligenceEnforcer()


def run_intelligence(payload: dict) -> dict:
    return enforcer.run(payload)
