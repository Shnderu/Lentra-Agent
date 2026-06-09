
from core.ai.planner.engine import AIPlanner

planner = AIPlanner()


def handle_ai_planner(text: str, user_id: int):

    result = planner.plan(text, user_id)

    return {
        "action": "queue",
        "task_id": result["task_id"],
        "type": "ai_planner"
    }
