from lentra.application.rent_search.service import (
    RentSearchApplicationService,
)


def build_main_router(container):

    service = RentSearchApplicationService(
        container.connector
    )

    class Router:

        async def handle(self, update: dict):

            if container.trace:
                container.trace.node("router_enter", update)

            intent = update.get("intent")

            if intent == "rent_search":

                if container.trace:
                    container.trace.node("route_rent_search")

                service.trace = container.trace

                return await service.search(
                    update.get("payload", {})
                )

            return {
                "text": "unknown intent"
            }

    return Router()
