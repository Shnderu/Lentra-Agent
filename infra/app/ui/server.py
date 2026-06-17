from http.server import SimpleHTTPRequestHandler, HTTPServer
import os


class UIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="app/ui/static", **kwargs)


def run():
    server = HTTPServer(("0.0.0.0", 3000), UIHandler)
    print("[UI] v9 running on http://localhost:3000")
    server.serve_forever()


if __name__ == "__main__":
    run()
