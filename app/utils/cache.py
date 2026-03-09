from app.core.redis import redis_client
import json
from typing import Any, Optional

DEFAULT_TTL = 60  # seconds

async def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL):
    redis = redis_client.redis
    if not redis:
        raise RuntimeError("Redis not initialized")

    await redis.set(cache_key(key), json.dumps(value), ex=ttl)


async def cache_get(key: str) -> Optional[Any]:
    redis = redis_client.redis
    if not redis:
        raise RuntimeError("Redis not initialized")

    data = await redis.get(cache_key(key))
    if data:
        return json.loads(data)
    return None


async def cache_delete(key: str):
    redis = redis_client.redis
    if not redis:
        raise RuntimeError("Redis not initialized")

    await redis.delete(cache_key(key))

def cache_key(*args: Any) -> str:
    return "cache:" + ":".join(map(str, args))