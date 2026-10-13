# Plan: port the HTML prototype into FastAPI + React

Source of truth for this port. Re-read after any context reset. Rules come from
[AGENTS.md](../AGENTS.md) ("Must not break") and [DESIGN.md](../DESIGN.md).

## Phases (one commit each)

1. **Content** — move prototype data (`DIS`, `CL`, `RED`, `Q3`, `Q4`, `ECO`, `FIND`, `BODY`, `ROUTES`, weights) into
   `backend/app/triage/content/infection/*.json`.
2. **Backend** — content loader, schemas, `scoring.py` (rule engine, ST), `advice.py` (route, warnings, summary),
   `vision.py` (photo skeleton), routes, `Screening` table + migration, tests. Delete template `items`.
3. **Client** — `scripts/generate-client.sh` regenerates the API client and copies a content snapshot to the FE.
4. **FE shell** — theme tokens, fonts, CSS port, mascot/scene SVGs, 3D buttons, card, options, modal, sfx.
5. **FE quiz** — home, data diri, stage 1 (emergency check in browser) + red route, stages 2–5.
6. **FE result** — thinking screen, result, QR + summary page, Mobile JKN, save with consent.
7. **FE auth + leftovers** — restyle login/signup, chronic placeholder, delete items UI.
8. **Review** — lint, tests, build, check 390/768/1440px, check "Must not break".

## Content files (`backend/app/triage/content/infection/`)

| File | Owner | What |
| --- | --- | --- |
| `flow.json` | DR (text) | who, sex, red flags, clusters, Q3, Q4, eco, findings, body regions, drug chips, routes, pain faces, `child_age_limit` |
| `diseases.json` | DR | 20 diseases: name, emoji, route, lab, care |
| `advice.json` | DR (+ST for analysis wording) | warning texts, todo per route, drug keywords, cross-check texts, analysis steps |
| `weights.json` | ST | all points and thresholds |

Text uses `**bold**` for emphasis (FE renders safely, no raw HTML).

## Option IDs (shared FE / BE / scoring)

- Routes: `green` · `yellow` · `special` · `red`
- Clusters: `A` `B` `C` `D` `E`
- Q3 option id = disease id; "none of these" = `none`
- Q4, eco, findings, body: prototype ids (`bb`, `kms`, `timur`, `danau`, `banjir`, `padat`, `kontak`, `mr`, `lidah` …, `head`, `ruq` …)
- Red flags: `syok` `darah` `ginjal` `napas` `otak` `dehidrasi` `rabies`; "none" = `none`

## API (`/api/v1/triage`)

- `GET /flows/{flow_id}` → `FlowPublic` (flow.json + public disease info). `chronic` → 404 until DR delivers.
- `POST /flows/{flow_id}/score` body `Answers` → `ScoreResult`. Stateless, nothing saved.
- `POST /screenings` body `{flow_id, answers, consent: true}` → saves anonymous answers + result. No user link.
- `GET /screenings` superuser only (ST exports test data).
- `POST /photo/analyze` multipart → `{available, findings}`. Skeleton: `available=false` until ST plugs a model.
  Photo never stored.

`Answers` (snake_case): `who, age, sex, red_flags[], complaint, pattern, companion[], eco[], drugs, temp, no_thermo,
height_cm, weight_kg, nutrition_proxy, body[], pain (0–10|null), findings[], province`.

`ScoreResult`: `unknown, route, top, ranked[≤4], candidates, top_pct, reasons[], cross_checks[], warnings[{level,icon,text}],
drug_warnings[], todo[], place, maps_query, analysis_steps[], summary`.

## Front end

- Routes: `/` home · `/skrining` quiz+thinking+result+red · `/ringkasan#d=…` QR page · `/kronis` placeholder ·
  `/login` `/signup` (restyled) · `/_layout/settings` `/_layout/admin` kept.
- Content: React Query `GET flow`; bundled snapshot `content.snapshot.json` as fallback so stage 1 works offline.
- Emergency check is pure FE: any red flag → red screen, no server call.
- Score: `POST score` (debounced) for the mascot meter; on q6 "Next" for drug warnings; on finish for result.
- QR: `/ringkasan#d=<base64url answers>`. Hash never reaches the server logs. Page decodes in browser and calls
  `POST score` on our own server (stateless). **Team decision:** AGENTS says "tanpa server"; scoring lives in Python,
  so the page needs our API. Nothing is stored.
- CSS: port prototype CSS to `src/styles/tropicek.css`; tokens in `index.css` mapped to shadcn theme. Light theme only.

## Changes from the prototype (must apply)

- No `.tag` disease labels under options; no "Mode Presentasi".
- No "XGBoost"/"probabilitas". "skor kecocokan".
- Red route: no confetti, no game sounds, call 119 button + copyable 119/112.
- Pain scale copied as is (no start value, 0–10).
- Photo step: consent first. No fake "AI scan" while the analyzer is a skeleton; user picks findings.
- Disclaimer on every result page. Never "diagnosis" except in the disclaimer negation.
- Remove "simulasi" wording where the feature is now real (login, QR).

## Skeletons for unclear parts

- `scoring.py`: `ScoringEngine` protocol, `RuleEngine` (prototype rules), `ModelEngine` stub for ST's model.
- `vision.py`: `PhotoAnalyzer` protocol, `UnavailableAnalyzer`; ST plugs a real one.
- Location: `Answers.province` + empty `weights.province`; FE `lib/location.ts` stub. No UI step yet (⏳ DR/ST).
- Chronic path: `/kronis` placeholder; backend 404 until content exists.
