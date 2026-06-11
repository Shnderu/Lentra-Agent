from enum import Enum


class TaskState(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PROCESSING = "processing"
    RETRYING = "retrying"
    FAILED = "failed"
    DLQ = "dead_letter"
    COMPLETED = "completed"


ALLOWED_TRANSITIONS = {
    TaskState.CREATED: [TaskState.QUEUED],
    TaskState.QUEUED: [TaskState.PROCESSING],
    TaskState.PROCESSING: [TaskState.COMPLETED, TaskState.RETRYING, TaskState.FAILED],
    TaskState.RETRYING: [TaskState.PROCESSING, TaskState.DLQ],
    TaskState.FAILED: [TaskState.DLQ],
}
