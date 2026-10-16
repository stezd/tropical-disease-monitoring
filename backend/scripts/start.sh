#! /usr/bin/env bash

set -e

# Run database migrations and seed initial superuser
bash scripts/prestart.sh

# Run the production server (reads $PORT). Uses uvicorn directly, not `fastapi run`:
# `fastapi run` has no switch to turn off the access log, and that log writes the
# client IP of every request into the host's logs. --no-access-log keeps IPs out.
# --proxy-headers: same as `fastapi run` (trusts X-Forwarded-* only from 127.0.0.1
# unless FORWARDED_ALLOW_IPS is set; set it if redirects come out as http).
# Workers default to 1: four uvicorn workers each load the full app, which
# overruns a small instance (0.5 GB RAM, e.g. Railway's Free plan). Raise it
# for larger instances with WEB_CONCURRENCY.
exec uvicorn app.main:app --no-access-log --proxy-headers --host 0.0.0.0 --port "${PORT:-8000}" --workers "${WEB_CONCURRENCY:-1}"
