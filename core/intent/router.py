from core.intent.classifier import classify
from core.fsm.flows.route_flow import start_route_flow

async def route(user_id: int, text: str):

    intent = classify(text)

    print("🎯 INTENT:", intent.name)

    if intent.name == "route_search":
        await start_route_flow(user_id)

        # ❌ НИКАКОГО UI ТЕКСТА
        return None

    return None
