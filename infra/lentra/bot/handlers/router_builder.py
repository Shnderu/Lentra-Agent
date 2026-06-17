from lentra.bot.features.rent_search.service import RentSearchService


def build_main_router(container):

    service = container.rent_search_service

    class Router:

        async def handle(self, update: dict):

            if container.trace:
                container.trace.node("router_enter", update)

            intent = update.get("intent")

            if intent == "rent_search":

                if container.trace:
                    container.trace.node("route_rent_search")

                # 🔥 FIX: inject trace into service
                service.trace = container.trace

                return await service.search(update.get("payload", {}))

            return {"text": "unknown intent"}

    return Router()
