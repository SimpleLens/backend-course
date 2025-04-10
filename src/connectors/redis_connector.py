import redis.asyncio as redis


class RegisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def close(self):
        await self.redis.close()

    async def set(self, key: str, value: str, ex: int = None):
        if ex:
            await self.redis.set(key, value, ex)
        else:
            await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        await self.redis.delete(key)
