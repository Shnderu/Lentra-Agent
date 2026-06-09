from core.shard.shard import get_shard

def pick_queue(task_id: str, queues: int = 4):
    return f"queue_{get_shard(task_id, queues)}"
