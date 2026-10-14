# AGENTS.md — TropiCare

Short guide for AI agents and developers. Team plan: [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) (suggestions, not strict rules).

## The app

Gamified quiz that screens Indonesian patients and tells them where to go.

- **Infection path** — 20 tropical diseases. Medical source of truth: [docs/Acuan-Medis.md](docs/Acuan-Medis.md)
  - **Photo step (low priority):** the infection path asks the user for a photo (e.g. rash, swelling). ST builds the analysis; if not ready, keep the prototype's simulated step. Photos are health data: ask consent, don't commit real photos to the repo.
- **Chronic path (PTM)** — same file (clusters F–H, CVD score, PTM routes). MedGemma input/output formats: [docs/Format-MedGemma.md](docs/Format-MedGemma.md)
- **Result** — a route: MERAH (IGD) · KUNING KHUSUS (program poli) · KUNING (Puskesmas) · HIJAU (self-care), plus a Mobile JKN button.

**Visual reference:** [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Colors, type, components: [DESIGN.md](DESIGN.md). Copy its look into React. Don't copy its known mistakes. The section "Fitur" below lists every feature and what still has to change.

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
- **API** (`/api/v1`): `GET /triage/flows/{flow_id}` · `POST /triage/flows/{flow_id}/score`
- **Emergency check runs in the browser.** Any danger sign → MERAH screen right away, even if the server is down.
- **Standalone.** No integrations that need a legal agreement or admin approval (SATUSEHAT, BPJS API, telemedicine providers, faskes systems). Plain links are fine (Google Maps search, opening Mobile JKN). Nothing is sent outside our own server.
- **Login is optional.** Guests can do the whole quiz. Offer login on the home page.
- **Ask age and sex first.** They change which questions and options appear.
- **Low score** → "belum dapat ditentukan" + route KUNING.

## Must not break

- Never say "diagnosis" to patients. Use "skrining" or "perkiraan".
- No disease names on answer options. Only on the result page.
- Red route: no animation. Show a call 119 button, plus 119 and 112 as text that can be copied.
- Pain scale: 0–10 with faces and labels, like the prototype. No starting value. Save 0–10.
- Every result page has a disclaimer: this is screening, not a doctor's diagnosis.
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

## Fitur (in Indonesian)

Semua fitur aplikasi, beserta alasannya. Simulasi HTML hanya contoh tampilan; kolom **Status** menunjukkan apa yang tinggal dipindahkan dan apa yang masih harus diubah.

Status: ✅ ada di simulasi, pindahkan ke React · 🔧 ada di simulasi, perlu diubah atau dibuat sungguhan · 🧪 hanya simulasi, sebut sebagai rencana · ⏳ belum ada atau menunggu konfirmasi

### Mulai

| Fitur        | Deskripsi                                                                                                             | Alasan                                        | Status         |
| ------------ | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | -------------- |
| Halaman awal | Pilih "Saya sedang sakit" (jalur infeksi) atau "Cek risiko penyakit jangka panjang" (jalur kronis). Ada tombol Masuk. | Dua jalur punya alur pertanyaan yang berbeda. | ✅             |
| Jalur kronis | Skrining risiko penyakit jangka panjang (PTM): klaster Gula & Saraf, Tekanan & Kepala, Sendi, atau "tidak ada keluhan"; faktor risiko; tensi, gula darah, lingkar perut. Alur di [docs/Acuan-Medis.md](docs/Acuan-Medis.md) §5. | Melengkapi skrining infeksi akut. | 🔧 alur dari Blueprint sudah jalan; bobot faktor risiko/tensi/gula dan skor CVD menunggu ST; rute angina, care, dan lab PTM perlu DR |
| Data diri | Siapa yang sakit (sendiri, anak, lansia, keluarga lain), usia, dan jenis kelamin. Perempuan ditanya status kehamilan (Blueprint Q1). Ditanya paling awal. | nama, kelamin, pekerjaan | ✅ batas usia pertanyaan hamil (10 th) perlu DR |

### Kuesioner jalur infeksi

| Fitur                                 | Deskripsi                                                                                                                                                                                                                                                                               | Alasan                                                                                                            | Status                                                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Tahap 1 · Tanda bahaya               | Daftar kondisi gawat. Satu saja dipilih → kuesioner berhenti, langsung ke rute MERAH. Dicek di browser.                                                                                                                                                                                | Mencegah kematian: kondisi gawat tidak boleh menunggu kuesioner selesai, dan harus tetap jalan walau server mati. | ✅                                                                                               |
| Tahap 2 · Keluhan utama              | 5 klaster: demam, napas, pencernaan, kulit, bengkak.                                                                                                                                                                                                                                    | Mengelompokkan 20 penyakit supaya pasien hanya menjawab pertanyaan yang relevan.                                  | ✅                                                                                               |
| Tahap 3 · Gejala dan gejala penyerta | Pertanyaan berubah sesuai klaster yang dipilih.                                                                                                                                                                                                                                         | Membedakan penyakit yang gejalanya mirip.                                                                         | ✅                                                                                               |
| Tahap 4 · Peta ekologi               | Riwayat 1–4 bulan terakhir: daerah, banjir, lingkungan padat, kontak TBC, imunisasi.                                                                                                                                                                                                   | Faktor risiko lingkungan menambah ketepatan skor.                                                                 | ✅                                                                                               |
| Tahap 4 · Lokasi pengguna            | Minta izin lokasi browser, lalu ubah jadi provinsi di browser dengan data batas provinsi yang ikut di aplikasi, tanpa layanan peta luar. Hanya provinsi yang dipakai dan disimpan, bukan titik koordinat. Kalau izin ditolak, pasien memilih provinsi sendiri atau lanjut tanpa lokasi. | Beberapa penyakit lebih sering di wilayah tertentu, misalnya malaria di Papua dan NTT. Lokasi ikut masuk ke skor. | ⏳ wilayah dan bobot per penyakit perlu persetujuan DR dan ST                                    |
| Tahap 4 · Riwayat obat | Ketik atau ketuk obat yang sudah diminum (opsional). Muncul peringatan: NSAID pada demam (merah), obat mampat pada diare/amebiasis (kuning), Amlodipine pada bengkak dan Captopril pada batuk (biru, Blueprint Q5). | Mencegah pasien meneruskan obat yang bisa memperburuk kondisi. | 🔧 teks pop-up NSAID dan obat mampat: pilih versi Blueprint atau jawaban no. 12–13 (DR, Acuan-Medis K6–K7) |
| Tahap 5 · Suhu tubuh | Isi suhu dalam °C, atau centang "tidak punya termometer" lalu jawab proksi: menggigil/keringat deras, nadi cepat saat istirahat (DR no. 1). | Banyak orang tidak punya termometer; skor tetap bisa dihitung dari pola demam. | ✅ bobot proksi menunggu ST (sekarang 0 poin) |
| Tahap 5 · Tinggi dan berat badan | Hitung IMT, atau jawab pertanyaan pengganti (pakaian longgar, kelebihan berat badan/obesitas, normal). | Status gizi ikut menentukan risiko keparahan; pertanyaan pengganti untuk yang tidak punya timbangan. | ✅ obesitas → risiko malaria berat dikonfirmasi DR (no. 2) |
| Tahap 5 · Peta nyeri                 | Ketuk bagian tubuh yang sakit atau bengkak di gambar tubuh.                                                                                                                                                                                                                             | Lokasi nyeri membantu membedakan penyakit, misalnya perut kanan atas atau sendi pergelangan.                      | ✅                                                                                               |
| Skala nyeri                           | Skala 0–10 vertikal di samping peta tubuh, dengan wajah dan label. Tanpa nilai awal. Disimpan 0–10.                                                                                                                                                                                   | Angka dan wajah memudahkan pasien memilih tingkat nyeri; tanpa nilai awal supaya pilihan tidak terpancing.        | ✅ ambang skor menunggu ST                                                                       |
| Tahap 5 · Foto | Foto ruam, luka, atau mata, lalu pilih temuan: 5 chip dari DR no. 17 (jalur kronis + benjolan sendi, lipatan leher hitam). Minta izin dulu. | Temuan fisik menambah ketepatan skor. | 🧪 analisis foto dibuat ST (prioritas rendah) |
| Penghitung kemungkinan                | Di gelembung maskot: "N kemungkinan" dan skor saat ini.                                                                                                                                                                                                                                 | Pasien melihat kemajuan, seperti permainan Akinator.                                                              | ✅                                                                                               |

### Analisis dan hasil

| Fitur                            | Deskripsi                                                                                                                                                                                                                                                            | Alasan                                                                                                          | Status                                                                                                                             |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Layar "Kak Tropi sedang menebak" | Animasi langkah analisis sebelum hasil keluar.                                                                                                                                                                                                                       | Memberi jeda dan menunjukkan apa yang diperiksa.                                                                | 🔧 teks "AI" dan "imputasi" disesuaikan dengan cara hitung ST                                                                      |
| Skor kecocokan                   | Perkiraan utama dan skor kecocokan dalam persen. Tanpa kata "probabilitas", "XGBoost", atau nama model.                                                                                                                                                                           | Hasil mudah dipahami, dan jujur soal cara hitungnya.                                                            | ✅                                                                                                                                 |
| Skor rendah                      | "Belum dapat ditentukan" → rute KUNING.                                                                                                                                                                                                                             | Kalau pola tidak jelas, lebih aman diperiksa langsung.                                                          | ✅                                                                                                                                 |
| Kemungkinan lain                 | 3 perkiraan berikutnya beserta skornya.                                                                                                                                                                                                                              | Pasien dan petugas melihat pilihan lain yang perlu dipikirkan. beserta label keyakinan agar pengguna tau        | ✅                                                                                                                                 |
| "Kenapa aku menebak ini?"        | Jawaban yang paling memengaruhi skor, dan perbandingan penyakit mirip (Tifoid vs DBD, Kusta vs Tinea, Diare vs Amebiasis).                                                                                                                                           | Transparan: pasien tahu dasar perkiraannya.                                                                     | ✅                                                                                                                                 |
| Rute rujukan | MERAH (IGD) · KUNING KHUSUS (poli program) · KUNING (Puskesmas) · HIJAU (perawatan mandiri). Demam ≥ 39,5 °C atau sistolik > 160 mmHg menaikkan HIJAU ke KUNING. Tanda Varicella berat menaikkan ke KUNING. | Inti aplikasi: memberi tahu pasien harus ke mana. | ✅ aturan suhu dikonfirmasi DR (no. 15); rute Lepto/STH/Hepatitis/Varicella berat masih menunggu DR (Acuan-Medis K1–K4) |
| Yang perlu dilakukan             | Daftar langkah sesuai rute dan perkiraan.                                                                                                                                                                                                                            | Pasien tahu apa yang dilakukan sekarang.                                                                        | ✅ teks medis perlu persetujuan DR                                                                                                 |
| Navigasi ke faskes               | Tombol membuka Google Maps ke apotek atau Puskesmas terdekat.                                                                                                                                                                                                        | Pasien langsung tahu lokasinya.                                                                                 | ✅ hanya tautan pencarian, tanpa daftar faskes sendiri                                                                             |
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
| Login opsional | Tamu bisa skrining sampai selesai. Tawaran masuk ada di halaman awal. | Tidak menghalangi orang yang sedang sakit. | 🔧 simulasi hanya menyimpan nama di perangkat; BE membuat akun sungguhan. Belum ada fitur simpan hasil atau riwayat. |
| Tanpa NIK/BPJS | Tidak pernah meminta NIK atau nomor BPJS.                             | Mengurangi risiko kebocoran data.          | ✅                                                                                                                   |

### Permainan dan tampilan

| Fitur                 | Deskripsi                                                                   | Alasan                                            | Status |
| --------------------- | --------------------------------------------------------------------------- | ------------------------------------------------- | ------ |
| Maskot Kak Tropi      | Maskot yang berbicara lewat gelembung teks.                                 | Suasana ramah, tidak menakutkan.                  | ✅     |
| Peta tahap            | Titik tahap di bagian atas layar.                                           | Pasien tahu sudah sampai mana.                    | ✅     |
| Suara, getar, konfeti | Bisa dimatikan di Pengaturan. Animasi mati kalau`prefers-reduced-motion`. | Terasa seperti permainan, tapi tetap bisa diatur. | ✅     |
| Responsif             | HP dulu, lalu desktop (≥ 640px). samakan tampilan tablet degnan desktop    | Kebanyakan pengguna memakai HP.                   | ✅     |

## Keputusan medis terbuka (in Indonesian)

Blueprint dan jawaban dokter sudah digabung di [docs/Acuan-Medis.md](docs/Acuan-Medis.md); aslinya diarsipkan di `docs/arsip/`. Semua yang masih menunggu DR atau ST ada di bagian 1 dokumen itu (K1–K29), termasuk konflik rute Lepto/STH/Hepatitis/Varicella berat (K1–K4), urutan Peta Ekologi (K5), dan teks pop-up obat serta penafian (K6–K9).

## Remember (in Indonesian)

- **Jujur soal "AI".** Model yang dipakai: **MedGemma** (large multimodal model) + **RAG** atas sumber literatur yang disetujui DR. Tidak memakai XGBoost. MedGemma dijalankan di **server sendiri**, bukan lewat API pihak luar, supaya aplikasi tetap berdiri sendiri dan tidak ada data keluar. Hasil diuji dengan kartu kasus dokter. Fitur foto (MedGemma multimodal) sebut sebagai rencana sampai selesai.
- **Rute MERAH tetap tanpa animasi dan suara** (keputusan tim; Blueprint sudah disesuaikan).
- **Tetap aturan tetap, bukan model:** pemeriksaan tanda bahaya di browser, naik ke KUNING bila suhu ≥ 39,5 °C, dan skor rendah → KUNING. Pembagian tugas MedGemma dan skor aturan: ST.
- **Uji coba pakai kartu kasus,** bukan data kesehatan asli peserta. Peserta mengisi survei kemudahan pakai (SUS).
- **Jangan pakai kata "diagnosis"** di aplikasi. Pakai "skrining" atau "perkiraan".
- **Jangan minta NIK atau nomor BPJS.**
- **Aplikasi berdiri sendiri.** Tidak terhubung ke SATUSEHAT, sistem faskes, atau layanan telemedisin, supaya tidak ada beban hukum dan administrasi.
