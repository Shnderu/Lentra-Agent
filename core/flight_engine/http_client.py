import aiohttp


class HttpClient:

    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def get(self, url, headers=None, params=None):

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, headers=headers, params=params) as resp:

                try:
                    return await resp.json()
                except:
                    text = await resp.text()
                    print("[HTTP ERROR BODY]", text)
                    return {}

    async def post(self, url, headers=None, data=None):

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(url, headers=headers, data=data) as resp:

                try:
                    return await resp.json()
                except:
                    text = await resp.text()
                    print("[HTTP ERROR BODY]", text)
                    return {}
