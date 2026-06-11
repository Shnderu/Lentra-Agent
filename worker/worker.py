import time
import sys

print("LENTRA WORKER STARTED", flush=True)

i = 0

while True:
    i += 1
    print(f"heartbeat {i}", flush=True)
    sys.stdout.flush()
    time.sleep(2)
