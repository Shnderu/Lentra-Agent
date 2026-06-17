from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.trace import Span
from app.core.dlq import DeadLetterQueue
from app.core.retry_policy import RetryPolicy


bus = EventBus(None, DeadLetterQueue(), RetryPolicy())


class Handler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode())

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
        user_id = body.get("user_id", "default")

        span = Span(trace_id="api_trace")

        event = Event(
            type="USER_MESSAGE",
            payload={
                "text": text,
                "user_id": user_id
            }
        )

        result = bus.publish(event, span, None)

        if hasattr(result, "to_dict"):
            response = result.to_dict()
        else:
            response = {"raw": str(result)}

        self._send(200, {
            "trace_id": "api_trace",
            "result": response
        })


def run():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("[API] v10.1 session layer started")
    server.serve_forever()


if __name__ == "__main__":
    run()
