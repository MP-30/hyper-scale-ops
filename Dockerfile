FROM python:3.12-slim
LABEL authors="aditya"

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

ENTRYPOINT ["uv" , "run", "uvicorn", "app.main:app"]

CMD ["--host", "0.0.0.0", "--port", "8000"]