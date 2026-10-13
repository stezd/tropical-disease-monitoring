# ---------- stage 1: build the frontend ----------
FROM oven/bun:1 AS frontend-build

WORKDIR /app

COPY package.json bun.lock /app/
COPY frontend/package.json /app/frontend/

WORKDIR /app/frontend

RUN bun install

COPY ./frontend /app/frontend

ARG VITE_API_URL=

RUN bun run build


# ---------- stage 2: build the Python environment ----------
# uv lives only in this stage, so it never reaches the runtime image. Deleting it
# in a later RUN would not shrink anything: the layer that COPYs it keeps the bytes.
#
# No --mount flags anywhere in this file: Railway's builder rejects every mount
# type except type=cache, and cache mounts need an id built from the service id,
# which cannot be baked into a committed Dockerfile. UV_NO_CACHE keeps uv's
# download cache out of the layer too (it was 250 MB).
FROM python:3.14-slim AS backend-build

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1

WORKDIR /app/

# Dependencies only. --no-dev keeps pytest/mypy/ruff out of the runtime venv.
COPY uv.lock pyproject.toml /app/
COPY ./backend/pyproject.toml /app/backend/
RUN uv sync --frozen --no-dev --no-install-workspace --package app

# Then the app package itself.
COPY ./backend/app /app/backend/app
RUN uv sync --frozen --no-dev --package app


# ---------- stage 3: runtime ----------
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/backend/

# The virtualenv is the only thing we need from the build stage
COPY --from=backend-build /app/.venv /app/.venv

COPY ./backend/scripts /app/backend/scripts

COPY ./backend/pyproject.toml ./backend/alembic.ini /app/backend/

COPY ./backend/app /app/backend/app

COPY --from=frontend-build /app/frontend/dist /app/backend/app/frontend

CMD ["bash", "scripts/start.sh"]