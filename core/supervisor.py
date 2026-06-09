import os
import time
import subprocess

WORKER_CMD = ["python", "/app/main.py"]

RESTART_LIMIT = 5
count = 0


def run():
    global count

    while True:
        print("[SUPERVISOR] starting worker")

        p = subprocess.Popen(WORKER_CMD)

        p.wait()

        count += 1

        print("[SUPERVISOR] worker crashed, restart:", count)

        if count >= RESTART_LIMIT:
            print("[SUPERVISOR] max restart reached → exit")
            break

        time.sleep(2)


if __name__ == "__main__":
    run()
