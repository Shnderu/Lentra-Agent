class TaskState:
    NEW = "new"
    PROCESSING = "processing"
    FAILED = "failed"
    RETRYABLE = "retryable"
    RECOVERING = "recovering"
    DONE = "done"
    DEAD = "dead"


ALLOWED_TRANSITIONS = {
    TaskState.NEW: {TaskState.PROCESSING},
    TaskState.PROCESSING: {TaskState.DONE, TaskState.FAILED},
    TaskState.FAILED: {TaskState.RETRYABLE, TaskState.DEAD},
    TaskState.RETRYABLE: {TaskState.RECOVERING},
    TaskState.RECOVERING: {TaskState.DONE, TaskState.FAILED},
}


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in ALLOWED_TRANSITIONS.get(from_state, set())
