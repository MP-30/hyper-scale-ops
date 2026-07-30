FROM python:3.12 AS builder
ARG VERSION=dev
ARG COMMIT_SHA=unknown

LABEL org.opencontainers.image.title="Hyper Scale Ops"
LABEL org.opencontainers.image.description="FastAPI application"
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.revision=$COMMIT_SHA
LABEL org.opencontainers.image.source="https://github.com/MP-30/hyper-scale-ops"
LABEL org.opencontainers.image.authors="Aditya Bhadauriya"

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# OPTIMIZATION: Copy uv binary from official image instead of pip installing it
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

# Compile bytecode here during build time to speed up runner startup
ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN uv cache clean

FROM python:3.12-slim AS runner

RUN groupadd -g 10001 appuser \
 && useradd -u 10001 -g appuser -s /usr/sbin/nologin appuser

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# This makes Python use my installed packages automatically without needing 'uv run'.
ENV PATH="/app/.venv/bin:$PATH"

# Copy my source code (make sure to use a .dockerignore to skip local .venv)
COPY . .

EXPOSE 8000

#COPY herokuStart.sh /app/herokuStart.sh
#
#RUN chmod +x /app/herokuStart.sh
#
#RUN chown -R appuser:appuser /app

RUN chmod +x /app/herokuStart.sh \
    && chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s \
            --timeout=5s \
            --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["/app/herokuStart.sh"]
