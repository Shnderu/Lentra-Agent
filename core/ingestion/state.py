from enum import Enum


class TaskStatus(str, Enum):
    QUEUED = "queued"
    CLAIMED = "claimed"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    RETRYING = "retrying"
    DLQ = "dlq"
