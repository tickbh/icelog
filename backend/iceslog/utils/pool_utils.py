from fastapi import Request
from redis.asyncio import ConnectionPool, Redis

_redis_cache_pool_dict = {}

async def get_redis_cache(db=0):
    from iceslog.core.config import settings
    global _redis_cache_pool_dict
    if not db in _redis_cache_pool_dict:
        pool = ConnectionPool.from_url(settings.REDIS_URL, db=db, decode_responses=True)
        _redis_cache_pool_dict[db] = pool
    return await Redis(connection_pool=_redis_cache_pool_dict[db], decode_responses=True)
