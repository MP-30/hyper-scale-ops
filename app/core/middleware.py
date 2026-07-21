import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import app_logger
from app.core.request_context import set_request_id


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        request_id = str(uuid.uuid4())

        set_request_id(request_id)

        start = time.perf_counter()

        app_logger.info(
            f"Incoming {request.method} {request.url.path}"
        )

        response = await call_next(request)

        duration = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        app_logger.info(
            f"Completed {response.status_code} "
            f"in {duration} ms"
        )

        response.headers["X-Request-ID"] = request_id

        return response