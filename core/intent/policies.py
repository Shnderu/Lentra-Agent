
PRIORITY = {
    "fsm_active": 100,
    "route_search": 80,
    "ai_planner": 70,
    "deal_search": 60,
    "watch_route": 50,
    "unknown": 10
}


def resolve(intent_name: str) -> int:
    return PRIORITY.get(intent_name, 0)
