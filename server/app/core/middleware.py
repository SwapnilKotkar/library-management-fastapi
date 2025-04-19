from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

limiter = Limiter(key_func=lambda request: request.client.host)
limiter_middleware = SlowAPIMiddleware


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
