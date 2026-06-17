class Bot:
    async def run(self, router):
        print("[BOT] RUN STARTED")
        # временно просто держим процесс живым
        import asyncio
        while True:
            await asyncio.sleep(60)


def build_bot():
    return Bot()
