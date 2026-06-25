FROM python:3.12-slim AS builder
LABEL authors="aditya bhadauriya"

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

RUN uv sync --frozen --no-dev

FROM python:3.12-slim AS runner

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# This makes Python use my installed packages automatically without needing 'uv run'.
ENV PATH="/app/.venv/bin:$PATH"

# Copy my source code (make sure to use a .dockerignore to skip local .venv)
COPY . .

EXPOSE 8000

# Fix ownership of copied files so appuser can read them
RUN chown -R appuser:appuser /app

USER appuser

# FIX: Run uvicorn directly since it is now in my PATH
ENTRYPOINT ["uvicorn", "app.main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
