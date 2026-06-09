from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, decode_responses=True)

STREAM = "flyrum:event:stream"


@app.route("/events")
def events():
    data = r.xrevrange(STREAM, count=50)

    return jsonify([
        {
            "id": d[0],
            "type": d[1][b"type".decode() if isinstance(b"type", bytes) else "type"],
        }
        for d in data
    ])


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
