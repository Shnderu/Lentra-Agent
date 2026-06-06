from core.engine.task_engine import safe_push_task


def add_route(user_id: int, route: str):
    return safe_push_task(
        "route",
        {
            "user_id": user_id,
            "route": route
        }
    )
