import json
from .redis_client import redis_client

DEFAULT_TTL = 60  # seconds


def cache_get(key):
    value = redis_client.get(key)
    if not value:
        return None
    return json.loads(value)


def cache_set(key, value, ttl=DEFAULT_TTL):
    redis_client.setex(
        key,
        ttl,
        json.dumps(value)
    )


def cache_delete(key):
    redis_client.delete(key)
