from core.fsm.context import set_state


async def start_route_flow(user_id: int):
    print("[FLOW] start_route_flow")

    set_state(user_id, "route_from")

    # ❌ НЕ возвращаем True
    return None
