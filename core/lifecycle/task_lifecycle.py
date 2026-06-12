from enum import Enum


class TaskStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    RETRY = "retry"
    DLQ = "dlq"


class TaskLifecycle:
    """
    Central state machine for all tasks in system.
    """

    ALLOWED_TRANSITIONS = {
        TaskStatus.CREATED: {TaskStatus.QUEUED, TaskStatus.FAILED},
        TaskStatus.QUEUED: {TaskStatus.PROCESSING, TaskStatus.FAILED, TaskStatus.DLQ},
        TaskStatus.PROCESSING: {TaskStatus.DONE, TaskStatus.RETRY, TaskStatus.FAILED},
        TaskStatus.RETRY: {TaskStatus.PROCESSING, TaskStatus.DLQ},
        TaskStatus.FAILED: set(),
        TaskStatus.DONE: set(),
        TaskStatus.DLQ: set(),
    }

    @staticmethod
    def can_transition(from_status: str, to_status: str) -> bool:
        try:
            f = TaskStatus(from_status)
            t = TaskStatus(to_status)
            return t in TaskLifecycle.ALLOWED_TRANSITIONS.get(f, set())
        except Exception:
            return False

    @staticmethod
    def assert_transition(from_status: str, to_status: str):
        f = TaskStatus(from_status)
        t = TaskStatus(to_status)

        if not TaskLifecycle.can_transition(from_status, to_status):
            raise ValueError(f"Invalid transition: {f} -> {t}")
