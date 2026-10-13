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
| `WEB_CONCURRENCY` | `1` (default) or `2` | Optional. `start.sh` defaults to 1; raise on a larger instance |

Generate secrets:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

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

Port handling needs no configuration: `fastapi run` reads the `PORT` environment variable, and Railway injects it.

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

- No SATUSEHAT, BPJS API, telemedicine, or faskes integrations — plain links only (Google Maps search, opening Mobile JKN).
- No NIK or BPJS numbers, ever.
- Photos are never stored; the photo analyzer is a skeleton returning `available: false`.
- Nothing is sent outside our own server.

See `AGENTS.md` for the full "Must not break" list.
