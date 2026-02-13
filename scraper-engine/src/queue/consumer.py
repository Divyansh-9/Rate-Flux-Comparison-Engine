"""Redis consumer – thin wrapper around the redis-py client."""

import redis as redis_lib
from loguru import logger

from src.config.settings import settings


def create_redis_client() -> redis_lib.Redis:
    """Create and return a blocking Redis client."""
    client = redis_lib.Redis.from_url(
        settings.redis_url, decode_responses=True
    )
    client.ping()
    logger.info(f"[redis] connected to {settings.redis_url}")
    return client
