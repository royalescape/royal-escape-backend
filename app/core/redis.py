from upstash_redis.asyncio import Redis
from app.core.config import settings

# upstash-redis uses HTTP, so no more TCP connection errors!
redis_client = Redis(
    url=settings.upstash_redis_rest_url, 
    token=settings.upstash_redis_rest_token
)

async def blacklist_token(jti: str, ttl_seconds: int):
    await redis_client.setex(f"jwt_blacklist:{jti}", ttl_seconds, 1)


async def is_token_blacklisted(jti: str) -> bool:
    return await redis_client.exists(f"jwt_blacklist:{jti}") == 1
