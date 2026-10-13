# AGENTS.md — TropiCek

Short guide for AI agents and developers. Team plan: [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) (suggestions, not strict rules).

## The app

Gamified quiz that screens Indonesian patients and tells them where to go.

- **Infection path** — 20 tropical diseases. Flow: [docs/Blueprint.md](docs/Blueprint.md)
  - **Photo step (low priority):** the infection path asks the user for a photo (e.g. rash, swelling). ST builds the analysis; if not ready, keep the prototype's simulated step. Photos are health data: ask consent, don't commit real photos to the repo.
- **Chronic path** — Flow: [docs/Blueprint-Kronis.md](docs/Blueprint-Kronis.md)
- **Result** — a route: MERAH (IGD) · KUNING KHUSUS (program poli) · KUNING (Puskesmas) · HIJAU (self-care), plus a Mobile JKN button.

**Visual reference:** [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Copy its look into React. Don't copy its known mistakes. Section 3 of the plan lists the changes.

## Where things are

| What                                  | Where                             |
| ------------------------------------- | --------------------------------- |
| Backend (FastAPI, SQLModel)           | `backend/app`                   |
| Frontend (React, Tailwind, shadcn/ui) | `frontend/src`                  |
| Questions, options, weights (JSON)    | `backend/app/triage/content/`   |
| Scoring (owned by ST)                 | `backend/app/triage/scoring.py` |
| API client — generated, don't edit   | `frontend/src/client`           |

Template leftovers (`items`, template README): delete, don't build on them.

## Commands

```bash
docker compose up -d db mailpit          # database + mail

# backend (from backend/)
uv sync
uv run bash scripts/prestart.sh          # migrations + seed
uv run fastapi dev                       # localhost:8000/docs
uv run bash scripts/test.sh              # tests
uv run bash scripts/lint.sh              # lint

# frontend (from repo root)
bun install
bun run dev                              # localhost:5173
bash scripts/generate-client.sh          # after API changes
```

## How it fits together

- **Quiz content lives in JSON**, not React. DR and ST edit it without FE. Option IDs are shared by FE, BE, and scoring; rename all three together.
- **API** (`/api/v1`): `GET /triage/flows/{flow_id}` · `POST /triage/flows/{flow_id}/score` · `POST /screenings` · `GET /screenings/me`
- **Emergency check runs in the browser.** Any danger sign → MERAH screen right away, even if the server is down.
- **Login is optional.** Guests can do the whole quiz. Offer login on the result page.
- **Ask age and sex first.** They change which questions and options appear.
- **Low score** → "belum dapat ditentukan" + route KUNING.

## Must not break

- Never say "diagnosis" to patients. Use "skrining" or "perkiraan".
- No disease names on answer options. Only on the result page.
- Red route: no coins or animation. Show a call 119 button, plus 119 and 112 as text that can be copied.
- Pain scale: plain line from "Tidak nyeri" to "Nyeri terburuk". No numbers, no starting position. Save 0–100.
- Every result page has a disclaimer: this is screening, not a doctor's diagnosis.
- Coins reward finishing and follow-up. Never specific answers.
- Medical text changes need DR's OK. Weight changes need ST's OK.
- **Privacy:** ask consent before saving. Never collect NIK or BPJS numbers. No real patient data in the repo. No real secrets in git.

## Mobile JKN button

- Android: `intent://#Intent;package=app.bpjs.mobile;S.browser_fallback_url=<Play Store URL>;end`
- Otherwise: `https://play.google.com/store/apps/details?id=app.bpjs.mobile`
- Test on a real Android phone before the demo.

## Tips

- Branch from `master`, keep PRs small, keep `master` working.
- Model changed → add an Alembic migration. API changed → regenerate the client.
- Design for phones first, then tablet (≥640px) and desktop (≥960px).
- Near the deadline: fix bugs instead of adding features.
