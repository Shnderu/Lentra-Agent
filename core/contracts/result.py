import json


class Result:
    @staticmethod
    def dumps(task_id: str, user_id: int, data: dict) -> str:
        return json.dumps({
            "task_id": task_id,
            "user_id": user_id,
            "data": data
        })

    @staticmethod
    def loads(raw: str):
        return json.loads(raw)
