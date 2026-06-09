import aiohttp
import asyncio


class HttpClient:

    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=8)

    async def get(self, url: str, params: dict = None, headers: dict = None):

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params, headers=headers) as resp:
                return await resp.json()

    async def post(self, url: str, json: dict = None, headers: dict = None):

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(url, json=json, headers=headers) as resp:
                return await resp.json()
