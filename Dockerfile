FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

RUN /root/.local/bin/uv sync --frozen --no-cache

COPY src ./src
COPY README.md ./

EXPOSE 8000

CMD ["/root/.local/bin/uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--chdir", "src"]
