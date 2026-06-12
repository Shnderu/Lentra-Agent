import os
import time

"""
Lentra Production Bootstrap v1

Единая точка входа:
- НЕ содержит бизнес-логики
- только маршрутизация режимов запуска
"""

MODE = os.getenv("LENTRA_MODE", "worker")


def start_worker():
    print(">>> BOOTSTRAP: WORKER MODE")
    from worker.worker import run
    run()


def start_api():
    print(">>> BOOTSTRAP: API MODE")
    from api.main import app
    return app


def start_bot():
    print(">>> BOOTSTRAP: BOT MODE")
    from bot.main import start_bot
    start_bot()


def main():
    print(">>> LENTRA BOOTSTRAP START")
    print(f">>> MODE = {MODE}")

    if MODE == "worker":
        start_worker()
    elif MODE == "api":
        start_api()
    elif MODE == "bot":
        start_bot()
    else:
        raise ValueError(f"Unknown LENTRA_MODE: {MODE}")


if __name__ == "__main__":
    main()
