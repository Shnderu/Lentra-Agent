from fastapi import APIRouter, WebSocket
from lentra.core.market_intelligence.stream.global_stream import get_stream

router = APIRouter()

stream = get_stream()


@router.websocket("/ws/stream")
async def stream_socket(websocket: WebSocket):
    await websocket.accept()

    queue = []

    def subscriber(event):
        queue.append(event)

    stream.subscribe(subscriber)

    try:
        while True:

            # send buffered events
            while queue:
                event = queue.pop(0)
                await websocket.send_json(event)

    except Exception:
        pass
