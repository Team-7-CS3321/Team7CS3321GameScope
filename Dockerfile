FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
    curl \
    gnupg \
  && curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh | sh \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync --frozen --no-dev

COPY backend/src/team7cs3321gamescope ./src/team7cs3321gamescope

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["doppler", "run", "--", "uv", "run", "uvicorn", "team7cs3321gamescope.main:app", "--host", "0.0.0.0", "--port", "8000"]
