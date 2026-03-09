import asyncio

import pytest

from app.core.config import settings
from app.core.redis import redis_client
from app.utils.cache import cache_delete, cache_get, cache_set
from app.utils.session import create_session, delete_session, get_session


#
# CACHE TESTS
#
@pytest.mark.asyncio
async def test_cache():
    await redis_client.connect(settings.REDIS_URL)

    """ensure clean state"""
    await redis_client.redis.flushdb()

    """SET THE VALUE"""
    await cache_set("test:key", {"x": 1}, ttl=5)

    """GET THE VALUE"""
    value = await cache_get("test:key")
    assert value == {"x": 1}

    """DELETE THE VALUE"""
    await cache_delete("test:key")
    assert await cache_get("test:key") is None

    """TTL TEST"""
    await cache_set("ttl:key", {"y": 2}, ttl=1)
    await asyncio.sleep(2)
    assert await cache_get("ttl:key") is None

    await redis_client.disconnect()


#
# REDIS TESTS
#
@pytest.mark.asyncio
async def test_session():
    await redis_client.connect(settings.REDIS_URL)

    """ensure clean state"""
    await redis_client.redis.flushdb()
    
    """SET THE SESSION"""
    session_id = await create_session(user_id=1211)
    assert session_id is not None

    """GET THE SESSION"""
    session = await get_session(session_id)
    assert session["user_id"] == 1211

    """DELETE THE SESSION"""
    await delete_session(session_id)
    assert await get_session(session_id) is None
