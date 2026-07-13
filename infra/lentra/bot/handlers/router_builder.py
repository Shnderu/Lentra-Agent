def build_main_router(container):

    class Router:

        async def handle(self, update: dict):

            if container.trace:
                container.trace.node(
                    "router_enter",
                    update
                )

            intent = update.get(
                "intent"
            )

            if intent == "rent_search":

                if container.trace:
                    container.trace.node(
                        "route_rent_search"
                    )

                return await container.rent_search_service.search(
                    update.get(
                        "payload",
                        {}
                    )
                )

            return {
                "text": "unknown intent"
            }

    return Router()
