import time
import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

print("LENTRA WORKER STARTED (STREAM MODE V6.3)")

while True:
    time.sleep(3)
    print("stream heartbeat OK")
