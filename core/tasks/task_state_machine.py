from typing import Literal


TaskStatus = Literal[
    "pending",
    "processing",
    "done",
    "sent",
    "failed"
]


class TaskStateMachine:

    @staticmethod
    def can_transition(from_status: TaskStatus, to_status: TaskStatus) -> bool:

        transitions = {
            "pending": ["processing", "failed"],
            "processing": ["done", "failed", "pending"],
            "done": ["sent"],
            "failed": ["pending"],
            "sent": []
        }

        return to_status in transitions.get(from_status, [])

    @staticmethod
    def assert_transition(from_status: TaskStatus, to_status: TaskStatus):
        if not TaskStateMachine.can_transition(from_status, to_status):
            raise ValueError(
                f"Invalid transition: {from_status} -> {to_status}"
            )
