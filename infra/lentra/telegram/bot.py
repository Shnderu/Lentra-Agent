import asyncio

from lentra.telegram.ux.router import build_router


class BotRuntime:
    def __init__(self):
        self.router = build_router()

    async def run(self):
        print("[BOOT] RUN LOOP STARTED")

        # имитация event loop
        while True:
            await asyncio.sleep(5)


def main():
    print("[BOOT] ENTER MAIN")

    bot = BotRuntime()

    print("[BOOT] SERVICE READY")

    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
