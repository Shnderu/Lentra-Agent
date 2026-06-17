class Router:
    def __init__(self):
        pass

    async def handle(self, update: dict):
        return {
            "text": "ok",
            "update": update
        }


def init_router():
    return Router()
