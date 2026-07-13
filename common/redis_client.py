import redis
from django.conf import settings

REDIS_HOST = getattr(settings, 'REDIS_HOST', 'redis')
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)
