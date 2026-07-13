from rest_framework.response import Response
from rest_framework import status
from .redis_client import redis_client

RATE_LIMIT = 100      # requests
RATE_WINDOW = 60      # seconds


def rate_limit(request):
    """
    Rate limit per authenticated user
    """
    if not request.user.is_authenticated:
        return None

    key = f"rate_limit:user:{request.user.id}"
    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, RATE_WINDOW)

    if current > RATE_LIMIT:
        return Response(
            {
                "error": "Rate limit exceeded",
                "detail": "Too many requests. Try again later."
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return None