import traceback
import logging
import subprocess

logging.basicConfig(level=logging.INFO)

print(">>> MAIN START")

try:
    from aiogram import Bot, Dispatcher
    print(">>> AIROGRAM OK")
except Exception:
    print(">>> BOOT ERROR:")
    traceback.print_exc()
    raise


def main():
    print(">>> STARTING SYSTEM")

    print(">>> STARTING WORKER PROCESS")

    # 🔥 FIX: correct container path is /app
    subprocess.Popen(["python3", "/app/worker_main.py"])

    print(">>> MAIN READY (BOOTSTRAPPED)")


if __name__ == "__main__":
    main()
