from dataclasses import dataclass
import json


@dataclass
class Task:
    id: str
    type: str
    payload: dict

    def dumps(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type,
            "payload": self.payload
        })

    @staticmethod
    def loads(raw: str):
        data = json.loads(raw)
        return Task(
            id=data["id"],
            type=data["type"],
            payload=data["payload"]
        )
