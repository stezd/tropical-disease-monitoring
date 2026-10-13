#! /usr/bin/env bash

set -e

# Run database migrations and seed initial superuser
bash scripts/prestart.sh

# Run FastAPI production server (reads $PORT automatically).
# Workers default to 1: four uvicorn workers each load the full app, which
# overruns a small instance (0.5 GB RAM, e.g. Railway's Free plan). Raise it
# for larger instances with WEB_CONCURRENCY.
exec fastapi run --workers "${WEB_CONCURRENCY:-1}"
