import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True,
)


async def blacklist_token(jti: str, ttl_seconds: int):
    await redis_client.setex(f"jwt_blacklist:{jti}", ttl_seconds, 1)


async def is_token_blacklisted(jti: str) -> bool:
    return await redis_client.exists(f"jwt_blacklist:{jti}") == 1
