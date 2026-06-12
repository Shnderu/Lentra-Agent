import hashlib

def get_shard(task_id: str, shards: int = 2) -> int:
    h = hashlib.sha256(task_id.encode()).hexdigest()
    return int(h, 16) % shards


def route_stream(task_id: str) -> str:
    shard = get_shard(task_id, 2)
    return f"stream:rent:tasks:shard:{shard}"
