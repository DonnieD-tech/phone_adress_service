import os
from typing import AsyncGenerator

import redis.asyncio as redis

REDIS_HOST = os.getenv(
    'REDIS_HOST',
    'localhost'
)
REDIS_PORT = int(
    os.getenv(
        'REDIS_PORT',
        6379
    )
)

redis_client: redis.Redis | None = None

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    global redis_client

    if redis_client is None:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT
        )

    try:
        yield redis_client
    finally:
        pass