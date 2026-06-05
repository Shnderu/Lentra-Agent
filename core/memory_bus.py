import asyncio
from collections import defaultdict

# in-memory event storage
_queues = defaultdict(asyncio.Queue)


def publish(channel: str, message: dict):
    """
    Push event into memory queue
    """
    if channel not in _queues:
        _queues[channel] = asyncio.Queue()

    _queues[channel].put_nowait(message)


async def subscribe(channel: str):
    """
    Async generator for events
    """
    if channel not in _queues:
        _queues[channel] = asyncio.Queue()

    while True:
        msg = await _queues[channel].get()
        yield msg
