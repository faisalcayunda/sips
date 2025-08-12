import os

from aiocache import SimpleMemoryCache


class CacheManager:
    """
    Class agnostik untuk handle operasi cache: get, set, delete.
    Menggunakan SimpleMemoryCache sebagai backend.
    """

    def __init__(self, ttl: int = None):
        self.ttl = ttl or int(os.getenv("CACHE_TTL", 300))  # default 5 menit
        self.cache = SimpleMemoryCache()

    async def get(self, key: str):
        return await self.cache.get(key)

    async def set(self, key: str, value, ttl: int = None):
        ttl = ttl or self.ttl
        await self.cache.set(key, value, ttl=ttl)

    async def delete(self, key: str):
        await self.cache.delete(key)


# Singleton instance
cache_manager = CacheManager()
