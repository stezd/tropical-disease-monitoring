# Triage content

Quiz text, options, and weights live here, not in React. The backend serves them at
`GET /api/v1/triage/flows/{flow_id}` and scores answers with them.

| File | Owner | Approve changes |
| --- | --- | --- |
| `infection/flow.json` | Questions, options, red flags, routes | DR |
| `infection/diseases.json` | 20 diseases: name, route, lab, care | DR |
| `infection/advice.json` | Warnings, todo lists, drug keywords, analysis wording | DR (analysis wording: ST) |
| `infection/weights.json` | Points and thresholds | ST |

## Rules

- **Option IDs are shared** by FE, BE, and scoring. Rename in all three together.
- Use `**bold**` for emphasis. No HTML.
- Never put disease names in option `text`. Only in `reason`, which shows on the result page.
- After editing `flow.json`, run `bash scripts/generate-client.sh` from the repo root. It copies a snapshot to the
  front end so the emergency check works offline. A backend test fails if the snapshot is stale.
- Run `uv run pytest tests/triage` in `backend/` after any change. The loader validates every ID.

## Open items (copied from the prototype TODOs)

- `child_age_limit` (18): DR, question no. 3 (cacingan only for children?).
- Pattern B: is a cough of exactly 14 days ISPA or TBC? DR.
- Typhoid has no option in cluster A (fever). DR + ST.
- Cross-check "Tifoid vs DBD" mentions petekie, but no question asks about it. DR + ST.
- `weights.province` is empty until DR names endemic provinces and ST sets weights (question no. 10).
- `advice.warnings.no_bmi` and `analysis_steps.no_bmi` still say "AI" / "imputasi". ST rewrites them to match the
  real scoring method.
- Chronic path: no content yet. Add `chronic/` with the same files when `docs/Blueprint-Kronis.md` exists.
