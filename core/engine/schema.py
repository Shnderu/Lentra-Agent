import uuid
import time

class Task:
    def __init__(self, task_type, payload, priority=5, retry=0):
        self.id = str(uuid.uuid4())
        self.type = task_type
        self.payload = payload
        self.priority = priority
        self.retry = retry
        self.created_at = int(time.time())

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "priority": self.priority,
            "retry": self.retry,
            "created_at": self.created_at
