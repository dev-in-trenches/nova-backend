import logging
from typing import Optional

import redis.asyncio as redis

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self, url: str | None):
        if url is None:
            logger.warning("No Redis URL provided")
            return

        try:
            self.redis = redis.from_url(
                url,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            await self.redis.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    async def disconnect(self):
        if self.redis:
            await self.redis.aclose()


redis_client = RedisClient()


