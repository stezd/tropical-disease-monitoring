# AGENTS.md — TropiCare

Short guide for AI agents and developers. Team plan: [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) (suggestions, not strict rules).

## The app

Gamified quiz that screens Indonesian patients and tells them where to go.

- **Infection path** — 20 tropical diseases. Medical source of truth: [docs/Acuan-Medis.md](docs/Acuan-Medis.md)
  - No photo step (removed by team decision, 2026-10-15).
- **Privacy gate** — right after choosing a path, the patient must tick the privacy consent before any question. Location is requested only after that tick.
- **Chronic path (PTM)** — same file (clusters F–H, CVD score, PTM routes). MedGemma input/output formats: [docs/Format-MedGemma.md](docs/Format-MedGemma.md)
- **Result** — a route: MERAH (IGD) · KUNING KHUSUS (program poli) · KUNING (Puskesmas) · HIJAU (self-care), plus a Mobile JKN button.

**Visual reference:** [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Colors, type, components: [DESIGN.md](DESIGN.md). Copy its look into React. Don't copy its known mistakes. The section "Fitur" below lists every feature and what still has to change.

## Where things are

| What                                  | Where                             |
| ------------------------------------- | --------------------------------- |
| Backend (FastAPI, SQLModel)           | `backend/app`                   |
| — API routes                          | `backend/app/api/routes/`         |
| — Use cases (orchestration)          | `backend/app/application/use_cases/` |
| — Domain rules (route, warnings, etc) | `backend/app/domain/`            |
| — Adapters (JSON disk, SQLModel DB)   | `backend/app/adapters/`          |
| — Composition root (wire-up / DI)     | `backend/app/composition/`       |
| Questions, options, weights (JSON)    | `backend/app/triage/content/`   |
| Scoring engines (Rule / Model)        | `backend/app/triage/scoring.py` |
| Frontend (React, Tailwind, shadcn/ui) | `frontend/src`                  |
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
bun run lint                             # biome: format + lint, rewrites files
bash scripts/generate-client.sh          # after API changes

# everything CI checks (from repo root)
uv run prek run --all-files              # pre-commit hooks over every file
```

## Lolos CI (sebelum push)

CI runs pre-commit only on the files a PR changes, and **treats a hook that rewrites a file as a failure**. Run these before pushing:

```bash
uv run prek run --all-files              # from repo root
uv run bash scripts/lint.sh              # from backend/
uv run bash scripts/test.sh              # from backend/
bun run lint && bun test                 # from repo root
```

- If prek or biome rewrites a file, `git add` it and commit again. This is the most common red CI.
- Words CI flags as typos but are real Indonesian (`maks`, `tabel`, `oktober`, …) live in `[tool.typos.default.extend-words]` in `pyproject.toml`. Add the word there, don't change the UI copy.
- `frontend/src/client/` and `frontend/public/data/` are generated/vendored and excluded from the formatters. Don't reformat them.

## Traps (don't rediscover these)

- **Use `127.0.0.1`, never `localhost`, in `DATABASE_URL`.** On Windows with Docker Desktop, `localhost` resolves to IPv6 `::1` first; the port forward accepts the SYN but never completes the handshake, so the OS waits out a ~21s TCP timeout before falling back to IPv4. One connection costs **~130s instead of ~0.015s**. This alone made the backend suite take 260s instead of 7s. `.env` and `.env.example` already use `127.0.0.1`. Linux CI is unaffected, so don't "fix" the workflow files.
- **`bash` does not work on Windows here.** It resolves to the WSL shim, and the default distro is `docker-desktop`, which has no `/bin/bash`. So `scripts/*.sh` fail, and the `generate-frontend-sdk` pre-commit hook is always red locally. Run the underlying command instead (`bun run generate-client` after dumping `openapi.json`), and expect that one hook to fail locally only.
- **Running `pytest` empties the `facility` mirror.** The `clean_facilities` fixture deletes every row on setup and teardown. Re-run `scripts/sync_facilities.py` after tests, before demoing, or the facilities endpoint returns an empty list. The same goes for `screening_stat`: the test fixtures delete every row, and stats rows cannot be rebuilt. **Never run `pytest` against a database that holds real stats** (check `DATABASE_URL`; the repo `.env` may point at Railway).
- **`except A, B:` without parentheses is valid on Python 3.14** (PEP 758). `ruff format` normalises to it. Don't "fix" it to `except (A, B):` — ruff will revert it.
- **`uv run` is not free.** It re-resolves the environment on every call. For a tight dev loop, activate `.venv` once and call `python -m pytest` directly. Also skip `scripts/test.sh` while iterating: it runs `coverage`, which instruments every line.

## How it fits together

- **Quiz content lives in JSON**, not React. DR and ST edit it without FE. Option IDs are shared by FE, BE, and scoring; rename all three together.
- **API** (`/api/v1`): `GET /triage/flows/{flow_id}` · `POST /triage/flows/{flow_id}/score`
- **Emergency check runs in the browser.** Any danger sign → MERAH screen right away, even if the server is down.
- **Data may leave our server** (e.g. to OpenRouter and Google for AI scoring); say so in the consent text.
- **Login is optional.** Guests can do the whole quiz, but personal history is not saved for them; the result page invites them to create an account. Signed-in users (email + password, or "Masuk dengan Google") can save a screening to their history (`/riwayat`) and delete it. Google sign-in is a normal login, not an integration that needs an agreement.
- **Statistics without direct identity (all users, guests too).** Every finished screening adds one row to `screening_stat`, separate from personal history. Fields enter only through an explicit whitelist in `backend/app/domain/screening_stat.py` (a new `Answers` field is not stored automatically). Never stored: user id, IP, exact age, raw vital numbers, drug text, coordinates, clock time. Aggregates hide groups < 10. Never call this data "anonim"; say "tanpa identitas langsung" (UU PDP still applies).
- **Location stays in the browser.** Coordinates (asked after the privacy tick) are used on the device for the province and the nearest facilities (up to 5); only the province goes to the server. Denied → the patient may pick a province, and the result page can ask again.
- **Max 3 fields per page.** A 4th field appears in the same card once the first three are filled (`.reveal-in`), or moves to its own step.
- **Ask age and sex first.** They change which questions and options appear.
- **Low score** → "belum dapat ditentukan" + route KUNING.
- **Low confidence** → top confidence (`top.pct`) below 80% (`refer_below_pct` in `weights.json`) raises GREEN to YELLOW with a see-a-doctor note. RED and KUNING KHUSUS are unchanged. ST must OK the value; DR must OK the note text.
- **Backend changes follow ports & adapters:**
  - Route handlers (`api/routes/triage.py`) stay dumb: parse the request, call `get_score_use_case().execute(...)`, return schemas.
  - Triage orchestration lives in `application/use_cases/score_flow.py`, not in route functions.
  - Business rules live in `domain/`: `route_policy.py` (which route wins), `warnings.py` (which alerts fire), `narration.py` (mascot bubble text), `answers.py` (raw intake).
  - Outbound data access lives in `adapters/` and implements the interfaces in `application/ports/`. Never import an adapter from `domain/`.
  - Wire-up happens in `composition/triage_container.py`. Swap engines or repositories there, not in application code.
  - Triage behavior is protected by frozen snapshot tests in `backend/tests/triage/test_goldens.py`. If a change intentionally alters scoring output for existing cases, update the corresponding `goldens/<name>.json`.

## Must not break

- Never say "diagnosis" to patients. Use "skrining" or "perkiraan".
- No disease names on answer options. Only on the result page.
- Red route: no animation. Show a call 119 button, plus 119 and 112 as text that can be copied.
- Pain scale: 0–10 with faces and labels, like the prototype. No starting value. Save 0–10.
- Every result page has a disclaimer: this is screening, not a doctor's diagnosis.
- Medical text changes need DR's OK. Weight changes need ST's OK.
- **Privacy:** consent gate before the first question. Two tiers: personal history only for signed-in users who press save; statistics without direct identity for every finished screening (see "Login is optional"). The consent text must stay in line with `Privacy.tsx`. Never call this data "anonim". No real patient data in the repo. No real secrets in git.

## Mobile JKN button

- Android: `intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;package=app.bpjs.mobile;S.browser_fallback_url=<Play Store URL>;end`
- Otherwise: `https://play.google.com/store/apps/details?id=app.bpjs.mobile`
- Mobile JKN 4.18.0 has no deep link (no URL scheme, no App Links; checked in its AndroidManifest). Chrome only opens apps that accept browser links, so in Chrome the button lands on the Play Store page, which shows "Buka" when the app is installed. If a later version adds a scheme, put it in `frontend/src/features/triage/links.ts`.
- Test on a real Android phone before the demo.

## Tips

- Branch from `master`, keep PRs small, keep `master` working.
- Model changed → add an Alembic migration. API changed → regenerate the client.
- Design for phones first, then tablet (≥640px) and desktop (≥960px).
- When checking UI, only check at 390px and 1440px.
- Near the deadline: fix bugs instead of adding features.

## Checklist aplikasi (in Indonesian)

- [ ] App bisa membuka Mobile JKN langsung saat di HP dan aplikasinya terpasang
- [ ] App bisa mengambil lokasi dan memasukkannya ke inferensi
- [ ] App melakukan inferensi secara akurat berdasarkan pilihan dan lokasi
- [ ] Tampilan enak di HP
- [ ] Pertanyaan lengkap
- [ ] Pemindai QR diarahkan ke halaman rangkuman yang ringkas, jelas, menarik, dan sederhana tanpa mengorbankan kualitas
- [ ] ~~Integrasi SATUSEHAT Master Sarana Index (MSI)~~ Tidak dilanjutkan (keputusan tim 16 Okt 2026). Mirror faskes yang sudah ada masih dipakai fitur "faskes terdekat"; nasibnya perlu diputuskan. Catatan teknis: [docs/SATUSEHAT.md](docs/SATUSEHAT.md).

## Fitur (in Indonesian)

Semua fitur aplikasi, beserta alasannya. Simulasi HTML hanya contoh tampilan; kolom **Status** menunjukkan apa yang tinggal dipindahkan dan apa yang masih harus diubah.

Status: ✅ ada di simulasi, pindahkan ke React · 🔧 ada di simulasi, perlu diubah atau dibuat sungguhan · 🧪 hanya simulasi, sebut sebagai rencana · ⏳ belum ada atau menunggu konfirmasi

### Mulai

| Fitur        | Deskripsi                                                                                                             | Alasan                                        | Status         |
| ------------ | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | -------------- |
| Halaman awal | Pilih "Saya sedang sakit" (jalur infeksi) atau "Cek risiko penyakit jangka panjang" (jalur kronis). Ada tombol Masuk. | Dua jalur punya alur pertanyaan yang berbeda. | ✅             |
| Jalur kronis | Skrining risiko penyakit jangka panjang (PTM): klaster Gula & Saraf, Tekanan & Kepala, Sendi, atau "tidak ada keluhan"; faktor risiko; tensi + gula darah sewaktu (GDS, patokan 200 mg/dL); pemeriksaan opsional asam urat + kolesterol total (langkah `labs`); tinggi, berat, lingkar perut; peta nyeri. Tensi >120 sampai <140 = "meningkat" (DR 15 Okt 2026). Maks 3 field per halaman. Alur di [docs/Acuan-Medis.md](docs/Acuan-Medis.md) §5. | Melengkapi skrining infeksi akut. | 🔧 alur dari Blueprint sudah jalan; bobot faktor risiko/tensi/gula dan skor CVD menunggu ST; rute angina, care, dan lab PTM perlu DR |
| Data diri | Siapa yang sakit (sendiri, anak, lansia, keluarga lain), usia, dan jenis kelamin. Perempuan ditanya status kehamilan (Blueprint Q1). Ditanya paling awal. | nama, kelamin, pekerjaan | ✅ batas usia pertanyaan hamil (10 th) perlu DR |

### Kuesioner jalur infeksi

| Fitur                                 | Deskripsi                                                                                                                                                                                                                                                                               | Alasan                                                                                                            | Status                                                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Tahap 1 · Tanda bahaya               | Daftar kondisi gawat. Satu saja dipilih → kuesioner berhenti, langsung ke rute MERAH. Dicek di browser.                                                                                                                                                                                | Mencegah kematian: kondisi gawat tidak boleh menunggu kuesioner selesai, dan harus tetap jalan walau server mati. | ✅                                                                                               |
| Tahap 2 · Keluhan utama              | 5 klaster: demam, napas, pencernaan, kulit, bengkak.                                                                                                                                                                                                                                    | Mengelompokkan 20 penyakit supaya pasien hanya menjawab pertanyaan yang relevan.                                  | ✅                                                                                               |
| Tahap 3 · Gejala dan gejala penyerta | Pertanyaan berubah sesuai klaster yang dipilih.                                                                                                                                                                                                                                         | Membedakan penyakit yang gejalanya mirip.                                                                         | ✅                                                                                               |
| Tahap 4 · Peta ekologi               | Riwayat 1–4 bulan terakhir: daerah, banjir, lingkungan padat, kontak TBC, imunisasi.                                                                                                                                                                                                   | Faktor risiko lingkungan menambah ketepatan skor.                                                                 | ✅                                                                                               |
| Gerbang privasi · Lokasi pengguna    | Setelah memilih jalur, pasien wajib mencentang persetujuan privasi (mencakup lokasi). Tanpa centang tidak bisa lanjut. Setelah dicentang, lokasi browser diminta otomatis (tanpa tombol "Pakai lokasiku"), lalu diubah jadi provinsi di browser dengan data batas provinsi yang ikut di aplikasi, tanpa layanan peta luar. Koordinat hanya di memori perangkat (untuk faskes terdekat); hanya provinsi yang dikirim ke server. Kalau izin ditolak, muncul pilihan provinsi (opsional). | Beberapa penyakit lebih sering di wilayah tertentu, misalnya malaria di Papua dan NTT. Lokasi ikut dipertimbangkan MedGemma. | ✅ lokasi → provinsi sudah jalan; provinsi masuk ke input MedGemma sebagai fakta "Provinsi tempat tinggal" ([docs/Format-MedGemma.md](docs/Format-MedGemma.md)), tanpa bobot per provinsi |
| Tahap 4 · Riwayat obat | Ketik atau ketuk obat yang sudah diminum (opsional). Muncul peringatan: NSAID pada demam (merah), obat mampat pada diare/amebiasis (kuning), Amlodipine pada bengkak dan Captopril pada batuk (biru, Blueprint Q5). | Mencegah pasien meneruskan obat yang bisa memperburuk kondisi. | ✅ teks pop-up versi gabungan (larangan, alasan, solusi), menunggu OK akhir DR (Acuan-Medis K6–K7) |
| Tahap 5 · Suhu tubuh | Isi suhu dalam °C, atau centang "tidak punya termometer" lalu jawab proksi: menggigil/keringat deras, nadi cepat saat istirahat (DR no. 1). | Banyak orang tidak punya termometer; skor tetap bisa dihitung dari pola demam. | ✅ bobot proksi menunggu ST (sekarang 0 poin) |
| Tahap 5 · Tinggi dan berat badan | Tinggi + berat badan; IMT dihitung di balik layar dan tidak ditampilkan ke pasien. Pertanyaan pengganti tetap ada (pakaian longgar, kelebihan berat badan/obesitas, normal). | Status gizi ikut menentukan risiko keparahan; pertanyaan pengganti untuk yang tidak punya timbangan. | ✅ obesitas → risiko malaria berat dikonfirmasi DR (no. 2) |
| Tahap 5 · Peta nyeri                 | Ketuk bagian tubuh yang sakit atau bengkak di gambar tubuh. Ada di jalur infeksi dan kronis; termasuk sendi bahu, siku, lutut (kanan/kiri) sesuai revisi DR 15 Okt 2026.                                                                                                                | Lokasi nyeri membantu membedakan penyakit, misalnya perut kanan atas atau sendi pergelangan.                      | ✅ bobot area sendi baru menunggu ST (sekarang 0)                                                |
| Skala nyeri                           | Skala 0–10 vertikal di samping peta tubuh, dengan wajah dan label. Tanpa nilai awal. Disimpan 0–10.                                                                                                                                                                                   | Angka dan wajah memudahkan pasien memilih tingkat nyeri; tanpa nilai awal supaya pilihan tidak terpancing.        | ✅ ambang skor menunggu ST                                                                       |
| Penghitung kemungkinan                | Di gelembung maskot: "N kemungkinan" dan skor saat ini.                                                                                                                                                                                                                                 | Pasien melihat kemajuan, seperti permainan Akinator.                                                              | ✅                                                                                               |

### Analisis dan hasil

| Fitur                            | Deskripsi                                                                                                                                                                                                                                                            | Alasan                                                                                                          | Status                                                                                                                             |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Layar "Kak Tropi sedang menebak" | Animasi langkah analisis sebelum hasil keluar.                                                                                                                                                                                                                       | Memberi jeda dan menunjukkan apa yang diperiksa.                                                                | 🔧 teks "AI" dan "imputasi" disesuaikan dengan cara hitung ST                                                                      |
| Skor kecocokan                   | Perkiraan utama dan skor kecocokan dalam persen. Tanpa kata "probabilitas", "XGBoost", atau nama model.                                                                                                                                                                           | Hasil mudah dipahami, dan jujur soal cara hitungnya.                                                            | ✅                                                                                                                                 |
| Skor rendah                      | "Belum dapat ditentukan" → rute KUNING.                                                                                                                                                                                                                             | Kalau pola tidak jelas, lebih aman diperiksa langsung.                                                          | ✅                                                                                                                                 |
| Kemungkinan lain                 | 3 perkiraan berikutnya beserta skornya.                                                                                                                                                                                                                              | Pasien dan petugas melihat pilihan lain yang perlu dipikirkan. beserta label keyakinan agar pengguna tau        | ✅                                                                                                                                 |
| "Kenapa aku menebak ini?"        | Jawaban yang paling memengaruhi skor, dan perbandingan penyakit mirip (Tifoid vs DBD, Kusta vs Tinea, Diare vs Amebiasis).                                                                                                                                           | Transparan: pasien tahu dasar perkiraannya.                                                                     | ✅                                                                                                                                 |
| Rute rujukan | MERAH (IGD) · KUNING KHUSUS (poli program) · KUNING (Puskesmas) · HIJAU (perawatan mandiri). Demam ≥ 39,5 °C atau sistolik > 160 mmHg menaikkan HIJAU ke KUNING. Gejala penyerta tertentu menaikkan rute: mata/kulit sangat kuning saat demam dan sesak pada Varicella → MERAH; Varicella dekat mata/bernanah dan anak cacingan lesu/pucat/perut buncit → KUNING. | Inti aplikasi: memberi tahu pasien harus ke mana. | ✅ aturan suhu dikonfirmasi DR (no. 15); rute Lepto/STH/Hepatitis/Varicella berat sudah diterapkan, menunggu OK akhir DR (Acuan-Medis K1–K4) |
| Yang perlu dilakukan             | Daftar langkah sesuai rute dan perkiraan.                                                                                                                                                                                                                            | Pasien tahu apa yang dilakukan sekarang.                                                                        | ✅ teks medis perlu persetujuan DR                                                                                                 |
| Navigasi ke faskes               | Sampai 5 faskes terdekat (diurutkan jarak di browser dari mirror MSI; yang punya WhatsApp lebih dulu). Tiap kartu: "Cari di Google Maps" dan "Kirim rangkuman via WhatsApp" (tautan wa.me berisi rangkuman skrining, dibuka pengguna sendiri) atau "Telepon" untuk nomor rumah/kantor. Tanpa lokasi: tombol "Lihat faskes terdekat" meminta izin lagi. | Pasien langsung tahu lokasinya dan bisa menghubungi faskes.                                                     | ✅ tautan biasa, server tidak mengirim apa pun                                                                                     |
| Tombol Mobile JKN                | "Buat janji dokter (Mobile JKN)". Android membuka aplikasinya, perangkat lain membuka Play Store.                                                                                                                                                                    | Lanjut ke pendaftaran resmi BPJS. Hanya membuka aplikasinya: tidak ada API, kerja sama, atau data yang dikirim. | ✅ uji di HP Android sungguhan                                                                                                     |
| Rangkuman dan salin | Rangkuman lengkap jawaban, bisa disalin. Memuat pemeriksaan lab yang mungkin dibutuhkan; lab tidak ditampilkan di halaman hasil. | Bisa dikirim atau ditunjukkan ke petugas. Petugas tahu pemeriksaan apa yang mungkin dibutuhkan. | ✅ lab DBD, Malaria, Tifoid, TBC dari DR (no. 21); lab penyakit lain perlu DR |
| QR rangkuman                     | QR di halaman hasil (rute selain HIJAU). Saat dipindai, terbuka halaman Rangkuman Pasien: kondisi pasien dan saran penanganan. Isi QR = alamat aplikasi + jawaban dalam kode ringkas, tanpa nama, NIK, atau foto. Halaman dihitung di browser petugas, tanpa server. | Petugas tidak perlu mengulang wawancara, tanpa terhubung ke sistem luar.                                        | 🔧 di simulasi sudah QR sungguhan. Teks saran penanganan perlu persetujuan DR. Di produksi, alamat QR = alamat aplikasi di server. |
| Catatan penting                  | Peringatan kuning, merah, atau biru (obat, suhu tinggi, data yang tidak diisi).                                                                                                                                                                                      | Hal penting tidak terlewat.                                                                                     | ✅                                                                                                                                 |
| Penafian                         | Di setiap halaman hasil: ini skrining, bukan diagnosis dokter.                                                                                                                                                                                                       | Wajib: aplikasi tidak menggantikan dokter.                                                                      | ✅                                                                                                                                 |

### Rute merah

| Fitur                        | Deskripsi                                                                   | Alasan                                                                        | Status                                                 |
| ---------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------ |
| Layar darurat                | Layar merah yang tenang. Tanpa animasi atau suara permainan.                | Keadaan serius; unsur permainan tidak pantas di sini.                         | ✅                                                     |
| Telepon 119                  | Tombol besar untuk menelepon 119, plus nomor 119 dan 112 yang bisa disalin. | Bantuan secepat mungkin; nomor bisa disalin kalau tombol telepon tidak jalan. | ✅                                                     |
| Kondisi terdeteksi | Kondisi yang dipilih, dengan pertolongan pertama (DO) dan larangan (DON'T) sambil menuju RS. Red flag PTM (jantung, stroke, krisis hipertensi, koma diabetik) tampil di kedua jalur. | Pasien tahu apa yang dilakukan selama perjalanan. | ✅ DO/DON'T Syok & Rabies dari DR (no. 19); fasilitas & pertolongan pertama red flag PTM perlu DR |
| Navigasi IGD / Rabies Center | Google Maps ke IGD, RS hemodialisa, atau Rabies Center sesuai kondisi.      | Tiap kondisi butuh fasilitas yang berbeda.                                    | ✅ hanya tautan pencarian, tanpa daftar faskes sendiri |
| "Salah pilih? Ubah jawaban"  | Kembali ke tahap 1.                                                         | Kalau tidak sengaja salah ketuk.                                              | ✅                                                     |

### Akun dan privasi

| Fitur          | Deskripsi                                                             | Alasan                                     | Status                                                                                                               |
| -------------- | --------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| Login opsional | Tamu bisa skrining sampai selesai, tapi riwayat pribadi tidak disimpan; di halaman hasil diajak "Buat akun" / "Masuk". Akun: email + password atau Masuk dengan Google. | Tidak menghalangi orang yang sedang sakit. | ✅ butuh `GOOGLE_CLIENT_ID` / `VITE_GOOGLE_CLIENT_ID` untuk tombol Google |
| Riwayat skrining | Pengguna login menekan "Simpan ke riwayatku"; daftar di `/riwayat`, bisa dihapus per item. Hapus akun = riwayat ikut terhapus. Terpisah dari itu, setiap skrining selesai (tamu juga) menambah satu baris statistik tanpa identitas langsung (`screening_stat`): tanpa akun, IP, usia pasti, angka vital, teks obat, koordinat, jam; agregat menyembunyikan kelompok < 10; tidak bisa dihapus per orang. | Pasien bisa melihat skrining sebelumnya; tim mendapat tren penyakit per wilayah. | ✅ teks privasi baru perlu OK DR (Acuan-Medis K35) |

### Permainan dan tampilan

| Fitur                 | Deskripsi                                                                   | Alasan                                            | Status |
| --------------------- | --------------------------------------------------------------------------- | ------------------------------------------------- | ------ |
| Maskot Kak Tropi      | Maskot yang berbicara lewat gelembung teks.                                 | Suasana ramah, tidak menakutkan.                  | ✅     |
| Peta tahap            | Titik tahap di bagian atas layar.                                           | Pasien tahu sudah sampai mana.                    | ✅     |
| Suara, getar, konfeti | Bisa dimatikan di Pengaturan. Animasi mati kalau`prefers-reduced-motion`. | Terasa seperti permainan, tapi tetap bisa diatur. | ✅     |
| Responsif             | HP dulu, lalu desktop (≥ 640px). samakan tampilan tablet degnan desktop    | Kebanyakan pengguna memakai HP.                   | ✅     |

## Keputusan medis terbuka (in Indonesian)

Blueprint dan jawaban dokter sudah digabung di [docs/Acuan-Medis.md](docs/Acuan-Medis.md); aslinya diarsipkan di `docs/arsip/`. Semua yang masih menunggu DR atau ST ada di bagian 1 dokumen itu, termasuk urutan Peta Ekologi (K5) dan teks penafian (K8–K9). Rute Lepto/STH/Hepatitis/Varicella berat (K1–K4) dan teks pop-up obat (K6–K7) sudah diputuskan dan diterapkan; DR tinggal memberi OK akhir.

## Remember (in Indonesian)

- **Jujur soal "AI".** Model yang dipakai: **MedGemma** (large multimodal model) + **RAG** atas sumber literatur yang disetujui DR. Tidak memakai XGBoost. Model boleh dipanggil lewat API pihak luar (Gemini atau OpenRouter/Gemma) atau dijalankan di server sendiri; data boleh keluar server, sebutkan di teks persetujuan. Hasil diuji dengan kartu kasus dokter. Fitur foto dihapus (keputusan tim 15 Okt 2026).
- **Rute MERAH tetap tanpa animasi dan suara** (keputusan tim; Blueprint sudah disesuaikan).
- **Tetap aturan tetap, bukan model:** pemeriksaan tanda bahaya di browser, naik ke KUNING bila suhu ≥ 39,5 °C, skor rendah → KUNING, dan keyakinan teratas < 80 % (`refer_below_pct`) menaikkan HIJAU ke KUNING dengan catatan periksa ke dokter (nilai: ST, teks: DR). Pembagian tugas MedGemma dan skor aturan: ST.
- **Uji coba pakai kartu kasus,** bukan data kesehatan asli peserta. Peserta mengisi survei kemudahan pakai (SUS).
- **Jangan pakai kata "diagnosis"** di aplikasi. Pakai "skrining" atau "perkiraan".
