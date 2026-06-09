import asyncio


async def retry(coro, attempts: int = 3, delay: float = 0.5):

    last_error = None

    for i in range(attempts):
        try:
            return await coro()
        except Exception as e:
            last_error = e
            await asyncio.sleep(delay * (i + 1))

    raise last_error
