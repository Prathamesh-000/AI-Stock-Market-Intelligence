"""Middleware modules for API request logging, rate limiting, and timing."""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("api.middleware")

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Measures and logs total HTTP request execution time."""
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time-Seconds"] = f"{process_time:.4f}"
        if request.url.path.startswith("/api/"):
            logger.debug(f"{request.method} {request.url.path} completed in {process_time*1000:.2f}ms")
        return response

__all__ = ["ProcessTimeMiddleware"]
