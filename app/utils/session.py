import json
import uuid

from app.core.redis import redis_client

SESSION_TTL = 60 * 60 * 24  # 1 day


async def create_session(user_id: int, ttl: int = SESSION_TTL):
    redis = redis_client.redis
    if not redis:
        raise Exception("Redis not initialized")

    session_id = str(uuid.uuid4())
    session_data = {"user_id": user_id}

    await redis.set(session_key(session_id), json.dumps(session_data), ex=ttl)

    return session_id


async def get_session(session_id: str):
    redis = redis_client.redis
    if not redis:
        raise Exception("Redis not initialized")

    data = await redis.get(session_key(session_id))
    if not data:
        return None
    return json.loads(data)


async def delete_session(session_id: str):
    redis = redis_client.redis
    if not redis:
        raise Exception("Redis not initialized")

    await redis.delete(session_key(session_id))

def session_key(session_id: str) -> str:
    return f"session:{session_id}"