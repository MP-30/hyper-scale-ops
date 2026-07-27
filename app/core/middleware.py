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

        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        app_logger.bind(
            event="request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=client_ip,
            user_agent=user_agent,
        ).info("Incoming request")

        try:
            response = await call_next(request)

            duration = round(
                (time.perf_counter() - start) * 1000,
                2,
            )

            app_logger.bind(
                event="request_completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration,
                client_ip=client_ip,
                user_agent=user_agent,
            ).info("Request completed")

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception:
            duration = round(
                (time.perf_counter() - start) * 1000,
                2,
            )

            app_logger.bind(
                event="request_failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                duration_ms=duration,
                client_ip=client_ip,
                user_agent=user_agent,
            ).exception("Unhandled exception")

            raise