from enum import IntEnum


class TaskPriority(IntEnum):
    LOW = 10
    NORMAL = 50
    HIGH = 80
    CRITICAL = 100
