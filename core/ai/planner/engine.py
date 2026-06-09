
from core.ai.planner.parser import parse_query
from core.ai.planner.builder import build_search
from core.queue.queue import enqueue


class AIPlanner:

    def plan(self, text: str, user_id: int):

        intent = parse_query(text)
        task = build_search(intent)

        task_id = enqueue(task["type"], task["payload"])

        return {
            "intent": intent,
            "task_id": task_id,
            "status": "queued"
        }
