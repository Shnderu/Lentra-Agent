# LENTRA TELEGRAM BOT - ADAPTER LAYER

from lentra.ux.scenarios import run_scenario


class Bot:
    """
    DI-compatible wrapper over functional UX layer
    """

    def __init__(self):
        pass

    async def run(self, router):
        """
        Compatibility entrypoint expected by container
        """
        # router уже собран выше, здесь просто держим контракт
        await router.start()


def handle_update(intent, payload, state):
    ux = run_scenario(intent, payload, state)

    return {
        "telegram_text": ux.get("text", ""),
        "ux": ux
    }
