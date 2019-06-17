import aioredis


class Redis:
    _redis = None

    async def get_redis_pool(self):
        if not self._redis:
            self._redis = await aioredis.create_redis_pool(('127.0.0.1', 6379), encoding='utf-8')
        return self._redis

    async def close(self):
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()


async def set_value(key, val):
    redis = Redis()
    r = await redis.get_redis_pool()
    await r.set(key, val)
    await redis.close()
    return True


async def get_value(key):
    redis = Redis()
    r = await redis.get_redis_pool()
    result = await r.get(key)

    await redis.close()
    return result
