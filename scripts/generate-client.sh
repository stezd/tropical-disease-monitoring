#! /usr/bin/env bash

set -e
set -x

cd backend
FASTAPI_ENV=development uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
# Offline copy of the quiz content for the front end (emergency check without server)
FASTAPI_ENV=development uv run python -m app.triage.snapshot
cd ..
mv openapi.json frontend/
bun run --filter frontend generate-client
bun run lint
