from enum import Enum


class TaskStatus(str, Enum):
    QUEUED = "queued"
    CLAIMED = "claimed"
    RUNNING = "running"
    RETRYING = "retrying"
    DONE = "done"
    FAILED = "failed"
    DLQ = "dlq"
