# Triage content

Quiz text, options, and weights live here, not in React. The backend serves them at
`GET /api/v1/triage/flows/{flow_id}` and scores answers with them. Flows: `infection`
(jalur infeksi) and `chronic` (jalur kronis / PTM).

| File | Owner | Approve changes |
| --- | --- | --- |
| `red_flags.json` | Danger signs + first aid, shared by every flow | DR |
| `<flow>/flow.json` | Steps, questions, options, routes | DR |
| `<flow>/diseases.json` | Diseases: name, route, lab, care | DR |
| `<flow>/advice.json` | Warnings, todo lists, drug rules, analysis wording | DR (analysis wording: ST) |
| `<flow>/weights.json` | Points and thresholds | ST |

## Rules

- **Option IDs are shared** by FE, BE, and scoring. Rename in all three together.
- Use `**bold**` for emphasis. No HTML.
- Never put disease names in option `text`. Only in `reason`, which shows on the result page.
- An option can point to several diseases with `diseases: [...]` (e.g. photo chips).
- Companion options can raise the route: `min_route` (at least that route), `red_flag`
  (a red flag ID: red screen right away, in the browser), and `staff_note` (a note for the
  doctor on the result and in the summary). A red flag with `"listed": false` is not in
  step 1; only a `red_flag` option reaches it.
- After editing any JSON, run `bash scripts/generate-client.sh` from the repo root. It copies a
  snapshot to the front end so the emergency check works offline. A backend test fails if the
  snapshot is stale.
- Run `uv run pytest tests/triage` in `backend/` after any change. The loader validates every ID.

## Source of truth

- Medical content (criteria, routes, text, and who approves what):
  [docs/Acuan-Medis.md](../../../../docs/Acuan-Medis.md). If a JSON file disagrees with it,
  the document wins.
- MedGemma input/output formats and the model scoring contract:
  [docs/Format-MedGemma.md](../../../../docs/Format-MedGemma.md).
- Open items for DR and ST: Acuan-Medis section 1 (K1–K29).
