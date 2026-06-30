from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/debug/ui")
def ui():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lentra AI OS Stream</title>
        <style>
            body { background:#0b0f14; color:#00ff9d; font-family: monospace; }
            .event { padding:5px; border-bottom:1px solid #1a1f27; }
        </style>
    </head>
    <body>

    <h3>AI OS STREAM</h3>
    <div id="log"></div>

    <script>
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/stream");
        const log = document.getElementById("log");

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);

            const div = document.createElement("div");
            div.className = "event";
            div.innerText = JSON.stringify(data);

            log.prepend(div);
        };
    </script>

    </body>
    </html>
    """
    return HTMLResponse(html)
