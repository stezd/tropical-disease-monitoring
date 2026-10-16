# Deploying TropiCare to Railway

One Railway **web service** + one Railway **PostgreSQL**. The web service builds `backend/Dockerfile`, which compiles the React frontend and serves it from the same origin as the API — so there is no second frontend service and no CORS configuration.

Verified locally on 2026-10-13: `docker compose build` exit 0, Playwright 53/53 against the built image, backend pytest 72/72.

---

## 1. Before you start: know which token you need

This is where most of the time goes, so read it first. Railway has **two** token types and they are **not** interchangeable:

| Token type | Where to create it | CLI variable | Can it… |
| --- | --- | --- | --- |
| **Account / workspace** token | Dashboard → avatar (top right) → **Account Settings** → **Tokens** | `RAILWAY_API_TOKEN` | create projects, list projects, everything |
| **Project** token | Dashboard → open the project → **Settings** → **Tokens** | `RAILWAY_TOKEN` | deploy, set variables, and act **inside that one project** |

Rules that cost us a debugging cycle:

- **A project token cannot create a project.** With one, `railway init` and `railway whoami` fail with `Unauthorized. Please check that your RAILWAY_TOKEN is valid and has access to the resource you're trying to use.` That message means *wrong scope*, not *bad token*.
- Diagnosis tip: query the token directly against the API. `me` failing while `projects` succeeds means project/workspace scope:

  ```bash
  curl -s -X POST https://backboard.railway.com/graphql/v2 \
    -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    --data-binary '{"query":"{ projects { edges { node { id name } } } }"}'
  ```

- **Set only one** of `RAILWAY_TOKEN` / `RAILWAY_API_TOKEN`. Setting both is an error.
- **Never paste a token into a chat or commit it.** Keep it in an untracked file and read it into the environment at runtime.

Full automation needs the **account token**. With a project token, create the project in the dashboard first (§2).

---

## 2. Create the project and database

Dashboard route (needed if you only have a project token):

1. **New Project → Empty Project**, name it `tropicare`.
2. **New → Database → PostgreSQL.**
3. Leave the database **private** (default). Do not add a TCP proxy — that only adds egress cost and exposure.

Then create the app service:

4. **New → Empty Service**, name it `backend`.
5. Open `backend` → **Variables** and add the table in §3 **before the first build**.

> If you skip step 5, the first build fails. Railway looks for `Dockerfile` at the **root of the source directory** and there isn't one — it will try Railpack auto-detection on the monorepo root and fail. `RAILWAY_DOCKERFILE_PATH` is what fixes it, and it must be set before the build runs.

> [!warning] Railway's builder supports **only** `--mount=type=cache`
> Any other mount type is rejected before the build even starts:
> `dockerfile invalid: flag '--mount=type=bind,...' is missing a type=cache argument (other mount types are not supported)`.
> Cache mounts additionally require `id=s/<service-id>-<target-path>`, which can't be baked into a committed Dockerfile. `backend/Dockerfile` therefore uses **no `--mount` flags at all** — it copies `uv.lock` and `pyproject.toml` into the image and runs `uv sync` against them.

---

## 3. Variables

Set these on the **`backend`** service:

| Variable | Value | Notes |
| --- | --- | --- |
| `RAILWAY_DOCKERFILE_PATH` | `backend/Dockerfile` | Required. Build context stays the repo root, which the Dockerfile needs |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Railway reference syntax. `app/core/config.py` rewrites `postgresql://` → `postgresql+psycopg://` |
| `PROJECT_NAME` | `TropiCare` | |
| `SECRET_KEY` | random, ≥32 bytes | See generation command below |
| `FIRST_SUPERUSER` | admin email | Used only for ST's screening-data export; login is optional for patients |
| `FIRST_SUPERUSER_PASSWORD` | random | |
| `FRONTEND_HOST` | `https://<domain>` | CORS allow-list. Cosmetic in the single-origin setup, but keep it correct |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID (Web) | Enables "Masuk dengan Google". Add the production domain to Authorized JavaScript origins |
| `TRIAGE_AI_CACHE_TTL_S` | optional | TTL (seconds, default 86400) of the in-memory AI result cache; `0` turns it off |
| `WEB_CONCURRENCY` | `1` (default) or `2` | Optional. `start.sh` defaults to 1; raise on a larger instance |

Generate secrets:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Frontend build-time variable:** `VITE_GOOGLE_CLIENT_ID` (same client ID) must be present when the image is built, because Vite inlines it. Changing it needs a rebuild.

**Migration on deploy:** Alembic revision `b7d2e4f19a6c` (adds `screening.user_id`) runs automatically via `prestart.sh` on the next deploy.

### Two traps

- **Do not set `FASTAPI_ENV=development`.** `backend/app/core/config.py` refuses to boot when `SECRET_KEY`, the `DATABASE_URL` password, or `FIRST_SUPERUSER_PASSWORD` is `changethis` — *unless* that flag is set, which downgrades it to a warning. Leaving it unset gives you the guard.
- Railway **suggests variables from `.env.example`** in the repo root. Don't blind-import them: they're all `changethis`, which is exactly what the guard rejects.

---

## 4. Deploy

### Dashboard

Deploy the `backend` service. Watch the build log for `Using detected Dockerfile!`.

### CLI

```bash
# account token: creates the project and services for you
export RAILWAY_API_TOKEN=<account token>
railway init --name tropicare
railway add --database postgres
railway add --service backend \
  --variables "RAILWAY_DOCKERFILE_PATH=backend/Dockerfile" \
  --variables "DATABASE_URL=\${{Postgres.DATABASE_URL}}" \
  --variables "PROJECT_NAME=TropiCare" \
  --variables "SECRET_KEY=<generated>" \
  --variables "FIRST_SUPERUSER=you@example.com" \
  --variables "FIRST_SUPERUSER_PASSWORD=<generated>"
railway up --service backend
railway domain --service backend
```

With a **project** token, replace `railway init` by linking to the project you created:

```bash
export RAILWAY_TOKEN=<project token>
railway link --project <project-id>
railway up --service backend
```

Notes:

- `railway up` uploads the **local directory**, so Railway never needs GitHub access to the repo. The trade-off: no autodeploy on push, deploys are explicit.
- `railway up` applies your **`.gitignore` patterns to the whole tree**, not just to untracked files. An over-broad pattern silently drops source files from the archive: a bare `lib/` excluded `frontend/src/lib/` and broke the TypeScript build with `TS2307`. Pre-flight by running `git check-ignore --no-index -v --stdin` over the output of `git ls-files` and confirm nothing you need is listed.
- **Do not trust `railway up`'s exit code.** In a non-interactive shell it returns 0 as soon as the upload finishes, before the build result is known — Railway's docs say it exits 0 only on SUCCESS, but we observed exit 0 while the deployment record said `FAILED`. Confirm with `railway deployment list --service backend`, then `railway logs --build -s backend` if it failed.
- `railway add --variables KEY=value` **echoes the values** in its output — we leaked two secrets that way and had to rotate them. Create the service first, then use `railway variable set`, which prints only the key names.
- The CLI **resolves** `${{Postgres.DATABASE_URL}}` to the literal connection string when you set it, so it will not follow a later database password rotation.
- `railway up` never exposes a service publicly — `railway domain` does that.
- Variable changes are **staged**; apply them with `railway redeploy`.

**Migrations run automatically.** `backend/scripts/start.sh` runs `scripts/prestart.sh` (`alembic upgrade head` + `initial_data.py`) before starting the server, so there is no pre-deploy step to configure. Keep the service at **one replica**: migrations at container start would race if two instances booted simultaneously.

---

## 5. Service settings worth setting

| Setting | Value | Why |
| --- | --- | --- |
| Healthcheck Path | `/api/v1/utils/health-check/` | Enables Railway's zero-downtime swap |
| Restart policy | `ON_FAILURE` | Avoids a crash loop burning usage |
| Domain port | leave default | The app reads Railway's injected `PORT` automatically and binds `0.0.0.0` |

Port handling needs no configuration: the server reads the `PORT` environment variable, and Railway injects it.

### Logs and client IPs

Every finished screening (guests too) adds a statistics row without direct identity, so client IPs must not end up in Railway logs.

- The server runs **without the access log** (`--no-access-log`, set in `backend/scripts/start.sh`), so request lines with client IPs are not written.
- No app code logs `request.client` or the `X-Forwarded-For` header. Keep it that way in review.
- Set Railway log retention to the shortest the plan allows (Project settings).
- After a deploy, check `railway logs`: no request lines with an IP address.

---

## 6. Verify

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/api/v1/utils/health-check/   # 200
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/                            # 200 (app shell)
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/docs                        # 200 (OpenAPI docs)
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/api/v1/triage/screenings    # 401 (superuser-only)
curl -s https://<domain>/api/v1/triage/flows/infection | head -c 200                  # flow JSON, 20 diseases
```

Then in a browser:

- [ ] Complete one quiz end to end → a result route appears
- [ ] Red route: any danger sign → red screen with a working 119 button (test with the API stopped too — this must not depend on the server)
- [ ] Mobile JKN button on a real Android phone
- [ ] One row lands in `screening` with **no** name, NIK, BPJS number, or photo
- [ ] Login works, using `FIRST_SUPERUSER` / `FIRST_SUPERUSER_PASSWORD`

Useful CLI: `railway logs`, `railway logs --build`, `railway connect` (database shell), `railway metrics`, `railway usage limit status`.

---

## 7. Local verification before you deploy

The same flow CI uses, which needs no Railway account:

```bash
docker compose build                                   # both images
docker compose down -v --remove-orphans                # wipes the local DB volume
docker compose run --rm backend bash scripts/prestart.sh
docker compose run --rm playwright bunx playwright test --fail-on-flaky-tests
```

Then browse the built image directly: `docker compose up -d db mailpit backend` → <http://localhost:8000>. Deep links like `/skrining` return 404 to `curl` without an `Accept: text/html` header — that is FastAPI's `app.frontend()` fallback behaving correctly for navigation requests, not a bug.

Windows notes: `bash` in this repo's scripts resolves to **WSL** via `cmd`, so run the underlying commands directly (`uv run alembic upgrade head`, `uv run python app/initial_data.py`). `uv sync` from `backend/` removes the root dev group (`prek`, `zizmor`) — restore with `uv sync` at the repo root.

---

## 8. Cost

| Plan | Price | Allowance |
| --- | --- | --- |
| Free | $0 | $1 of usage credit/month — **not enough** for Postgres + a web service |
| Hobby | $5/month | includes $5 of usage |
| Pro | $20/month | includes $20 of usage |

Rates: RAM $10/GB/month, CPU $20/vCPU/month, egress $0.05/GB. **Builds are free.** Two small services at ~0.5 GB RAM each lands around **$5–10/month** total. Set a spend limit.

---

## 9. Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Build fails, Railpack mentions no start command / a build error at the repo root | No root `Dockerfile` | Set `RAILWAY_DOCKERFILE_PATH=backend/Dockerfile` and redeploy |
| `dockerfile invalid: flag '--mount=type=bind,…' is missing a type=cache argument (other mount types are not supported)` | Railway's builder accepts only `type=cache` mounts | Remove every `--mount` flag from the Dockerfile and `COPY` the lock files instead |
| `error TS2307: Cannot find module '@/lib/utils'` during the image build | Root `.gitignore` has bare patterns such as `lib/` that match source directories at any depth, and `railway up` applies ignore patterns to the whole tree | Anchor them (`/lib/`) and pre-flight: run `git check-ignore --no-index -v --stdin` over the output of `git ls-files` |
| `error TS2307: Cannot find module './routeTree.gen'` plus cascading route-type errors | `frontend/src/routeTree.gen.ts` is gitignored and absent from a clean checkout, but `main.tsx` imports it and the build ran `tsc` first | Keep the build script as `vite build && tsc -p tsconfig.build.json`: the TanStack plugin generates the tree from its existing vite config before type-checking, and a type error still fails the build |
| `railway up` exited 0 but nothing is running | The exit code is not a success signal (observed) | `railway deployment list --service backend`, then `railway logs --build -s backend -n 60` |
| `railway status --service x` → `unexpected argument '--service'` | `status` is one of the few commands without the global service flag | Use `railway logs -s`, `railway deployment list -s`, `railway variable list -s` |
| `Unauthorized. Please check that your RAILWAY_TOKEN is valid…` | Project token used for an account-level command (or vice versa) | Use the right variable for the token's scope (§1) |
| `failed to resolve source metadata for ghcr.io/astral-sh/uv` | Registry DNS blip on the builder | Retry the build; it is transient, not your Dockerfile |
| `ValueError: The value of SECRET_KEY is "changethis"…` | Real secret not set, and `FASTAPI_ENV` unset | Set a real `SECRET_KEY` (do not set `FASTAPI_ENV=development`) |
| App boots then exits complaining about the database | Postgres not added, or `DATABASE_URL` not referencing it | `DATABASE_URL=${{Postgres.DATABASE_URL}}` |
| `config plan` refuses with "already managed by railway.json" | Legacy Config as Code | New services can't use `railway.json` — configure via dashboard/CLI. CaC files stop being read on **2026-12-01** |
| Healthcheck fails but `/` works | Wrong healthcheck path | Use `/api/v1/utils/health-check/` |
| Emails (password reset) silently do nothing | `SMTP_HOST` / `EMAILS_FROM_EMAIL` unset → `emails_enabled` is false | Configure SMTP if password reset must work |

---

## 10. What this app deliberately does not do

- No BPJS API, telemedicine, or faskes integrations — plain links only (Google Maps search, opening Mobile JKN).
- No photo feature: it was removed by team decision on 2026-10-15, so no images are uploaded or stored.
- Screening text may be sent to the Gemini API for AI scoring (stated in the consent text). SATUSEHAT integration is under consideration and not covered by this rule.

See `AGENTS.md` for the full "Must not break" list.

## 11. Image size (measured 2026-10-13)

The first Railway image was **2.45 GB**, which is why its build/export phase took about 20 minutes. After the size work it is **358 MB** - 85% smaller.

| Component | Before | After | Why |
| --- | --- | --- | --- |
| Base OS | `python:3.14` (~1.05 GB of apt layers) | `python:3.14-slim` | buildpack-deps (compilers, git, headers) is not needed: every dependency ships a wheel |
| uv download cache | 250 MB | 0 | `UV_NO_CACHE=1`, and the multi-stage split discards the build stage |
| uv + uvx binaries | 53 MB | 0 | they now live only in the build stage. Deleting them in a later `RUN` would NOT have shrunk anything - the layer that copied them keeps the bytes |
| Dev tooling (pytest, mypy + a 36 MB mypyc .so, ruff, pygments) | ~90 MB | 0 | `uv sync --no-dev` |
| Python venv | 297 MB | 134 MB | the above, applied |
| The React app | 1.1 MB | 1.1 MB | it was never the problem |

Two consequences worth knowing:

- **The runtime image has no `curl`**, so the backend healthcheck in `compose.yml` now uses a Python one-liner instead. Railway runs its own HTTP healthcheck, so nothing changes there.
- The Dockerfile is three stages: frontend build -> Python build (which owns `uv`) -> runtime (copies only `/app/.venv`). Keep `uv` out of the runtime stage.

Re-measure with `docker images backend:latest --format "{{.Size}}"`.

## 12. Production deploys require human approval

The gate is **branch-based**, not a toggle:

| Environment | Source branch | Trigger |
| --- | --- | --- |
| `development` | `master` | every push to `master` deploys automatically |
| `production` | `prod` | only a push to `prod` deploys |

The gate action is therefore **fast-forwarding `master` into `prod`** - explicit, visible, and reviewable:

```bash
git checkout prod
git merge --ff-only master
git push origin prod
```

How the wiring works:

- The `backend` service is connected to `stezd/tropical-disease-monitoring` via the Railway GitHub App.
- The **branch is per environment** and lives on a Railway **deployment trigger** (one row per environment), not on the service. A `serviceConnect` mutation creates the trigger rows; the branch is then set per environment on those rows. The dashboard exposes the same thing under Service Settings.
- **Connecting a repo - or changing its source - deploys every environment immediately.** Do it while the branches hold identical commits, or accept that production deploys whatever `prod` points at.
- `Wait for CI` (`checkSuites`) is **off**. It became possible on 2026-10-14, when the repository's GitHub Actions workflows finally registered - they had never been registered since the repo was created, and pushing a change under `.github/workflows/` fixed it. Left off for now: a failing check should not silently block a deploy until the suite has a track record.
- `railway up -e production` still works as an emergency path, but it uploads the local working tree rather than a committed revision. Prefer the branch, so what is deployed is always traceable to a commit.

## 13. When a deploy triggers (watch paths)

Both environments build only when something the image actually depends on changes:

```
backend/**
frontend/**
package.json
bun.lock
uv.lock
pyproject.toml
```

A docs-only or workflow-only commit is **skipped**: the service keeps its previous deployment instead of rebuilding a 358 MB image for a README edit. The root `package.json`/`bun.lock`/`uv.lock`/`pyproject.toml` are included because the Dockerfile copies them into the build.

Watch paths live on the **service instance**, so they are set per environment - changing them means updating `development` and `production` separately. A skipped push still records a deployment, with status `SKIPPED` (visible in `railway deployment list`), and the service keeps running its previous deployment - so a `SKIPPED` entry is the expected result for a docs-only commit, not a failure.

## 14. The `facility-sync` cron service

A **second service** in the project mirrors the SATUSEHAT Master Sarana Index into the `facility` table (see [docs/SATUSEHAT.md](docs/SATUSEHAT.md)). It is a normal Railway service with a cron schedule, not a separate scheduler primitive: Railway starts the container on schedule, runs the start command, and stops it when the process exits.

Exists in **both** environments, as a separate service instance per environment (§12's branch gate): `facility-sync` in `development`, `facility-sync-prod` in `production`, both created 2026-10-14.

| Setting | Value |
| --- | --- |
| Source | `stezd/tropical-disease-monitoring` |
| `RAILWAY_DOCKERFILE_PATH` | `backend/Dockerfile` (same image as the web app) |
| Start command | `python scripts/sync_facilities.py --include-apotek` |
| Cron schedule | `0 19 * * *` = **02:00 WIB**. Railway cron is always UTC - this offset is deliberate, not a typo |
| Restart policy | `NEVER` - it must not restart after finishing |
| Auto-deploy | **off** |

Variables are **references**, not copies, so no secret is duplicated:

```
DATABASE_URL            = ${{Postgres.DATABASE_URL}}
PROJECT_NAME            = ${{fullstack.PROJECT_NAME}}
SECRET_KEY              = ${{fullstack.SECRET_KEY}}
FIRST_SUPERUSER         = ${{fullstack.FIRST_SUPERUSER}}
FIRST_SUPERUSER_PASSWORD= ${{fullstack.FIRST_SUPERUSER_PASSWORD}}
SATUSEHAT_ENV           = ${{fullstack.SATUSEHAT_ENV}}
SATUSEHAT_CLIENT_ID     = ${{fullstack.SATUSEHAT_CLIENT_ID}}
SATUSEHAT_CLIENT_SECRET = ${{fullstack.SATUSEHAT_CLIENT_SECRET}}
SATUSEHAT_ORG_ID        = ${{fullstack.SATUSEHAT_ORG_ID}}
```

`SECRET_KEY` and `FIRST_SUPERUSER*` are required only because `sync_facilities.py` imports `app.core.config`, which validates them at import. Referencing the app's real values avoids the `changethis` guard.

Inspect, trigger, and watch:

```bash
railway cron list -s facility-sync -e development     # schedule + recent runs
railway cron run  -s facility-sync -e development -y  # off-schedule run ("Run now" in the dashboard)
railway logs      -s facility-sync -e development --since 2026-10-14T16:52:20Z
```

`--include-apotek` adds Apotek (105) so the HIJAU route can offer a pharmacy. It grows the mirror from ~13.900 to ~67.000 rows and the run from ~10 s to a couple of minutes (~78 pages). Only 2,1% of Apotek rows carry coordinates; the app passes `?with_coords=true` when ranking so the coordinate-less majority is never fetched. A healthy run ends with `Sync complete. Total facilities synced: <count>`, where `<count>` is now on the order of 67.000.

`development`'s `facility-sync` already uses this start command. **`production`'s `facility-sync-prod` still runs the plain `python scripts/sync_facilities.py`** and needs the same one-line change when Apotek should be mirrored in production too.

### Enabling server-side nearest ranking

The front end accepts `VITE_FACILITIES_SERVER_NEAREST` as a build arg (`backend/Dockerfile`). Set it on the **`fullstack`** service and redeploy so the built bundle uses `POST /facilities/nearest` (coordinates leave the device; see [docs/SATUSEHAT.md §3](docs/SATUSEHAT.md)). Without it, ranking happens in the browser and coordinates never leave the device. Either way the cron only mirrors data — it never serves requests, so do **not** set this variable on `facility-sync`.

### Three traps

- **Editing `sync_facilities.py` does not update the cron.** Auto-deploy is off (deliberately, so pushes don't rebuild a 358 MB image), so the cron keeps running its old image until someone triggers a deploy. Redeploy the service after changing the script.
- **`variableUpsert` queues a deployment per variable unless `skipDeploys: true` is set.** Setting ten variables without it queued ten sequential builds and the service sat `QUEUED` for four minutes. Pass `skipDeploys: true`, or set variables before the first deploy.
- **The cron builds the whole web Dockerfile**, frontend stages included, even though it only runs a Python script. Harmless (built once, reused by every run) but it makes the first build a couple of minutes. A slim `backend/Dockerfile.cron` that skips the frontend stages would fix it if more cron jobs are added.

**Migrations are not this service's job.** `fullstack` runs `alembic upgrade head` on boot (§4), so the `facility` table exists before the first sync. If the cron ever runs against a database where the table is missing, it fails with `UndefinedTable` rather than creating it.
