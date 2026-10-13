#! /usr/bin/env bash

set -e

# Run database migrations and seed initial superuser
bash scripts/prestart.sh

# Run FastAPI production server (reads $PORT automatically)
exec fastapi run --workers 4
