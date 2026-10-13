# AGENTS.md — TropiCek

Short guide for AI agents and developers. Team plan: [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) (suggestions, not strict rules).

## The app

Gamified quiz that screens Indonesian patients and tells them where to go.

- **Infection path** — 20 tropical diseases. Flow: [docs/Blueprint.md](docs/Blueprint.md)
  - **Photo step (low priority):** the infection path asks the user for a photo (e.g. rash, swelling). ST builds the analysis; if not ready, keep the prototype's simulated step. Photos are health data: ask consent, don't commit real photos to the repo.
- **Chronic path** — Flow: [docs/Blueprint-Kronis.md](docs/Blueprint-Kronis.md)
- **Result** — a route: MERAH (IGD) · KUNING KHUSUS (program poli) · KUNING (Puskesmas) · HIJAU (self-care), plus a Mobile JKN button.

**Visual reference:** [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Colors, type, components: [DESIGN.md](DESIGN.md). Copy its look into React. Don't copy its known mistakes. The section "Changes to make vs. the HTML prototype" below lists them.

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

## Changes to make vs. the HTML prototype (in Indonesian)

Simulasi HTML hanya contoh tampilan. Perubahan ini dibuat di aplikasi asli:

1. **Halaman awal:** pilih "Saya sedang sakit" atau "Cek risiko penyakit jangka panjang".
2. **Usia dan jenis kelamin** ditanya paling awal.
3. **Kondisi gawat:** tampilkan tombol telepon 119 dan nomor 119/112 yang bisa disalin. Tanpa koin atau animasi.
4. **Nama penyakit tidak muncul di pilihan jawaban,** hanya di halaman hasil.
5. **Skala nyeri** diganti dengan visual analogue scale
6. **Tombol "Buat janji dokter (Mobile JKN)"** di halaman hasil.
7. **Login opsional.** Orang tetap bisa skrining tanpa akun.
8. **Koin tidak diberikan per jawaban.** Koin untuk menyelesaikan skrining, kontrol setelah berobat, atau cek rutin.

## Open questions for the doctor (in Indonesian)

1. **Suhu tubuh:** kalau pasien tidak punya termometer di keluhan selain demam (napas, perut, kulit, bengkak), cukup tanya "Badan terasa panas?"?
2. **Tifoid:** di Blueprint ada kurung kosong "( )". Apakah isinya "pola demam naik bertahap"?
3. **Campak** masuk rute mana?
4. **"Badan gemuk → malaria berat":** ada sumbernya? Kalau tidak, dihapus.
5. **Peringatan jangan minum Ibuprofen/Aspirin** untuk dugaan DBD: setuju ditambahkan?
6. **Cacingan:** pilihan ini hanya untuk anak (batas usia berapa) atau semua umur?
7. **Bengkak menahun:** perlu pertanyaan tambahan supaya tidak langsung dianggap filariasis?
8. **Cacar air ringan vs. berat:** apa bedanya, dan yang berat dirujuk ke mana?
9. apakah ada vignette
10. **Tulisan "XGBoost"** di Blueprint diganti sesuai cara hitung ST.

## Remember (in Indonesian)

- **Jujur soal "AI".** Skor dihitung dari data literatur dan diuji dengan kartu kasus dokter. Fitur foto (kalau belum selesai), GPS, dan kirim data ke SATUSEHAT masih simulasi, jadi sebut sebagai rencana.
- **Uji coba pakai kartu kasus,** bukan data kesehatan asli peserta. Peserta mengisi survei kemudahan pakai (SUS).
- **Jangan pakai kata "diagnosis"** di aplikasi. Pakai "skrining" atau "perkiraan".
- **Jangan minta NIK atau nomor BPJS.**
