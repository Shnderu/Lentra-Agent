class TaskState:
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    RETRY = "retry"
    DEAD = "dead"


ALLOWED_TRANSITIONS = {
    PENDING: [PROCESSING],
    PROCESSING: [DONE, FAILED, RETRY, DEAD],
    RETRY: [PROCESSING],
}


def can_transition(current: str, next_state: str) -> bool:
    return next_state in ALLOWED_TRANSITIONS.get(current, [])
