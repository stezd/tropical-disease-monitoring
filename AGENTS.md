# AGENTS.md — TropiCek

Guide for AI coding agents (Claude Code, Codex, Cursor, etc.) and developers working in this repo.
Team plan, owners and deadlines live in [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) — read it before picking up work.

## What this project is

**TropiCek** is a hackathon prototype: a warm, gamified (Quizizz/Akinator-style) **self-screening and triage app** for Indonesian patients.

- **Infectious path** — adaptive triage for 20 tropical infections & NTDs (DBD, malaria, TBC, kusta, filariasis, …). Clinical flow: [docs/Blueprint.md](docs/Blueprint.md).
- **Chronic path** (new) — risk screening for a small set of chronic diseases. Spec: [docs/Blueprint-Kronis.md](docs/Blueprint-Kronis.md) (written by the team doctor).
- Output is a **referral route**: MERAH (IGD) · KUNING KHUSUS (program poli) · KUNING (Puskesmas) · HIJAU (self-care/apotek), plus a link to **Mobile JKN** to book a doctor.

### Reference prototype

[docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html) is a single-file HTML prototype of the full infectious flow. It is the **visual and UX reference** (colors, card-with-tab, 3D buttons, mascot "Kak Tropi", coins, stage map, layouts for <640px / ≥640px / ≥960px). Port it to React; do not keep developing the HTML file except for quick demos.

Known deviations of the prototype from the agreed design (fix them in the React port, not by copying the prototype): see section 7 of [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md). In particular its scoring in `compute()` is a hand-tuned baseline, its "XGBoost" label is not true, it shows disease labels on options, and its pain slider is a 0–10 numeric scale, not a VAS.

## Stack and layout

Based on the Full Stack FastAPI Template.

| Part                     | Tech                                                                                  | Path                              |
| ------------------------ | ------------------------------------------------------------------------------------- | --------------------------------- |
| Backend                  | FastAPI, SQLModel, PostgreSQL, Alembic, JWT auth (Python ≥3.14,`uv`)               | `backend/app`                   |
| Frontend                 | React 19, TypeScript, Vite, TanStack Router + Query, Tailwind v4, shadcn/ui (`bun`) | `frontend/src`                  |
| API client               | Generated from OpenAPI —**never edit by hand**                                 | `frontend/src/client`           |
| Triage content & weights | JSON, single source of truth for questions, options, weights                          | `backend/app/triage/content/`   |
| Scoring model            | Python module owned by the statistician                                               | `backend/app/triage/scoring.py` |

Template leftovers (`Item` model, `items` routes/pages, template README/release notes) should be removed or replaced, not extended.

## Commands

```bash
# services
docker compose up -d db mailpit

# backend (from backend/)
uv sync
uv run bash scripts/prestart.sh        # migrations + initial data
uv run fastapi dev                     # http://localhost:8000, docs at /docs
uv run bash scripts/test.sh            # pytest
uv run bash scripts/lint.sh            # mypy + ruff
uv run alembic revision --autogenerate -m "msg"   # after model changes

# frontend (from repo root)
bun install
bun run dev                            # http://localhost:5173
bun run lint                           # biome
bash scripts/generate-client.sh        # regenerate API client after backend API changes
```

## Architecture rules

1. **Content is data, not code.** Questions, options, flow order, and scoring weights live in `backend/app/triage/content/<flow>.json`. The doctor and statistician must be able to change wording/weights without touching React. Option IDs are the contract between frontend, backend, and the model — never rename an ID without updating all three.
2. **Endpoints** (prefix `/api/v1`):
   - `GET /triage/flows/{flow_id}` → questions for `infeksius` or `kronis` (no weights).
   - `POST /triage/flows/{flow_id}/score` → ranked results, route, reasons.
   - `POST /screenings` / `GET /screenings/me` → save and list a user's sessions (login optional).
3. **Emergency check is client-side and first.** A question marked `"emergency": true` routes to MERAH in the frontend as soon as any non-"none" option is chosen — no network call, no model, no login. Never make the red route depend on the backend being up.
4. **Login never blocks triage.** Guest mode is the default. Offer login/register on the result page to save history. Profile data pre-fills age/sex when logged in.
5. **Age and sex are asked first** (step "Siapa yang sakit?", before the emergency question), because they change which options are shown (e.g. child-only options) and the chronic risk scores.
6. **Scoring output is a "skor kecocokan", not a probability or diagnosis.** If the score is below threshold, return "belum dapat ditentukan" and route KUNING.

## Clinical-safety and UX rules (non-negotiable)

- UI copy is **Bahasa Indonesia**, warm and plain. Use "skrining", "perkiraan", "kemungkinan" — **never "diagnosis"** in patient-facing text.
- **No disease labels on answer options** in patient mode (they cause fear). Disease names appear only on the result page.
- The **red route shows no gamification** (no coins, confetti, badges). It shows: call 119 (`tel:119`), the numbers 119 and 112 as copyable text (desktop cannot dial), navigation to the nearest IGD, and first-aid tips.
- Pain/severity uses a **Visual Analogue Scale**: continuous 0–100 line, anchors "Tidak nyeri" and "Nyeri terburuk", no numbers or ticks shown, no default position until touched (avoid anchoring at the middle). Store the 0–100 value.
- Every result page carries the disclaimer that this is a screening and not a doctor's diagnosis.
- Points/coins reward **completion and healthy follow-up actions**, never specific answers, and never repeated screening of the same complaint.
- Clinical content and weights change only with approval from the doctor (content) or statistician (weights).

## Privacy

- Health data is "data pribadi spesifik" under UU PDP No. 27/2022: ask explicit consent before saving, collect the minimum (name, birth date or age, sex, kab/kota). **Do not collect NIK or BPJS card numbers.**
- No real patient data in the repo, seeds, screenshots, or tests. Use the doctor's clinical vignettes.
- `.env` in the repo contains placeholder values only (`changethis`). Real secrets go in the deployment environment, never in git.

## Mobile JKN hand-off

Result page CTA "Buat janji dokter (Mobile JKN)":

- Android: `intent://#Intent;package=app.bpjs.mobile;S.browser_fallback_url=<Play Store URL>;end` (opens the app if installed, else Play Store).
- Fallback / desktop: `https://play.google.com/store/apps/details?id=app.bpjs.mobile`.
- The package ID must be verified on a real Android phone before the demo.

## Working conventions

- Default branch on GitHub is `master`. Branch from it: `fe/<topic>`, `be/<topic>`, `stat/<topic>`, `content/<topic>`. Small PRs, merge often; no half-done work on `master` after Wednesday's deploy.
- After changing backend models: write an Alembic migration. After changing the API: regenerate the frontend client in the same PR.
- Backend: type hints everywhere, mypy strict passes, pytest for scoring and routing logic (test each route color with at least one vignette).
- Frontend: mobile-first (360–430px), then ≥640px and ≥960px layouts. Reuse shadcn/ui primitives, style them to match the prototype tokens.
- Feature freeze: **Thursday 15 Oct, 20:00 WIB**. After that only bug fixes, copy fixes, and README.
