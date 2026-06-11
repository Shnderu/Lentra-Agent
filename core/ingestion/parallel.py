import asyncio


class AsyncExecutor:

    def __init__(self, sources: dict):
        self.sources = sources

    async def _run(self, source, payload):
        try:
            return await asyncio.to_thread(source.search, payload)
        except Exception:
            return []

    async def run(self, source_names: list[str], payload: dict):
        tasks = []

        for name in source_names:
            source = self.sources.get(name)
            if not source:
                continue

            tasks.append(self._run(source, payload))

        results = await asyncio.gather(*tasks)
        flat = []

        for r in results:
            flat.extend(r)

        return flat
