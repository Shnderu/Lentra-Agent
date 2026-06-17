from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_intelligence_handler,
    rent_fetch_handler,
    rent_aggregate_handler,
    response_handler,
    unknown_handler
)
from app.core.trace import Span
from app.core.dlq import DeadLetterQueue
from app.core.retry_policy import RetryPolicy


# ⚠️ минимальная инстанция (изоляция от main)
bus = EventBus(None, DeadLetterQueue(), RetryPolicy())


class Handler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok"})
            return

        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/message":
            self._send(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length"))
        body = json.loads(self.rfile.read(length))

        text = body.get("text", "")

        span = Span(trace_id="api_trace")

        event = Event(type="USER_MESSAGE", payload={"text": text})

        # pipeline entry
        result = bus.publish(event, span, None)

        self._send(200, {
            "result": str(result),
            "trace_id": "api_trace"
        })


def run():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("[API] v8 server started on :8080")
    server.serve_forever()


if __name__ == "__main__":
    run()
