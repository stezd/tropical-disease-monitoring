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
- After editing any JSON, run `bash scripts/generate-client.sh` from the repo root. It copies a
  snapshot to the front end so the emergency check works offline. A backend test fails if the
  snapshot is stale.
- Run `uv run pytest tests/triage` in `backend/` after any change. The loader validates every ID.

## Open items

Scoring (ST):
- New questions score **0 points** until ST sets weights: no-thermometer and no-BP proxies
  (`vital_proxies`), blood pressure, blood sugar, waist, pregnancy, chronic risk factors
  (`chronic/weights.json` `eco: {}`).
- `chronic/weights.json` copies the generic infection numbers (complaint 10, pattern 40, …).
- CVD risk score (Blueprint Tahap 7): skeleton `scoring.cvd_risk()` returns None.
- `weights.province` is empty. DR named endemic provinces (Jawaban no. 10); ST sets weights.
- `advice.warnings.no_bmi`, `analysis_steps.no_bmi`, and the Amlodipine/Captopril pop-ups
  (Blueprint text, kept verbatim) say "AI" / "imputasi". Rewrite to match the real method (ST + DR).

Medical text (DR):
- Chronic: route for `angina` (set to yellow), care for every PTM disease except gout (uses the
  Blueprint lifestyle line), lab list (same full Blueprint PTM list for all), `no_bp` warning.
- PTM red flags: `facility` for all four, first aid for `krisis_ht` and `koma_dm` (not in Blueprint).
- `pregnancy_from_age` (10): from what age to ask about pregnancy?
- Severe varicella goes to the default Puskesmas place. Jawaban no. 8 says FKRTL/specialist,
  Blueprint says Puskesmas (AGENTS.md conflict no. 3).
- Drug names in care text vs. DR's safe list (Jawaban no. 18): Albendazol (`sth`),
  Klotrimazol (`tinea`), kalamin (`varicella`).
- Should a fast pulse at rest (no-thermometer proxy, "tanda SIRS") raise the route like ≥ 39.5 °C?
- Pattern B: is a cough of exactly 14 days ISPA or TBC?
- Typhoid has no option in cluster A (fever). DR + ST.
- Cross-check "Tifoid vs DBD" mentions petekie, but no question asks about it. DR + ST.
- Photo chips: the five DR chips replaced the prototype's nine, so tongue (typhoid), burrows
  (scabies), and ring rash (tinea) no longer score from the photo step.
