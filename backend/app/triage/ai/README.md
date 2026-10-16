# AI service triase (`app/triage/ai`)

Model bahasa menilai kandidat penyakit dari fakta pasien dan potongan literatur. `RuleEngine` tetap jadi jaring pengaman: kalau model gagal, hasil tetap keluar dari aturan, dengan penanda bahwa itu fallback.

## Cara menyalakan

```bash
# .env (di root repo)
TRIAGE_SCORING_ENGINE=ai
TRIAGE_AI_API_KEY=<kunci dari Google AI Studio>
TRIAGE_AI_RPM_LIMIT=<batas per menit yang tertera di AI Studio>
```

Tanpa API key, engine `ai` tetap jalan dan selalu memakai aturan (`reason=model_off`). Jadi aman di-deploy sebelum kunci tersedia.

Uji sekali dengan kunci sungguhan sebelum uji pengguna:

```bash
cd backend
TRIAGE_AI_API_KEY=... python scripts/ai_smoke.py
```

## Pintu masuk

| Cara | Untuk |
|---|---|
| `TRIAGE_SCORING_ENGINE=ai` | `POST /triage/flows/{flow_id}/score` langsung memakai model. Tidak ada kode backend yang perlu diubah. |
| `get_ai_engine().score(answers, content)` | Impor langsung. Hasilnya `AIBreakdown` = `ScoreBreakdown` + `meta`. |
| `POST /api/v1/ai/score` | Lewat HTTP: skor, alasan, sumber, dan penanda fallback. Superuser saja, karena setiap panggilan memakai kuota model. |
| `GET /api/v1/ai/status` | Model, mode, pemakaian kuota lokal. Superuser saja. |

## Alur

1. `build_request()` (kontrak ST di `Gemma4.py`) mengubah jawaban jadi fakta F1..Fn. Ada tanda bahaya: model tidak dipanggil.
2. Teks obat pasien **tidak dikirim**. Obat punya langkah sendiri (`/drugs`, menyusul), supaya Paracetamol tidak menurunkan skor DBD.
3. Literatur diambil dari `data/<flow>_literature.json` (dihitung offline, tanpa embedding saat runtime). Setiap potongan diberi label ID penyakit, dan model hanya menerima potongan tentang kandidatnya.
4. Model juga menerima daftar **"Ditanyakan, tidak dipilih"**. Form tidak punya pilihan negasi, jadi inilah cara model tahu sebuah gejala ditanyakan dan tidak ada.
5. Keluaran dikunci JSON Schema, lalu divalidasi lagi: ID kandidat, F-ID, dan S-ID yang tidak ditawarkan dibuang dan dihitung (`invalid_ids`). Di mode single, sumber yang dikutip untuk penyakit lain juga dibuang.
6. `to_breakdown()` (kontrak ST) mengubahnya ke `ScoreBreakdown`. Teks alasan untuk pasien tetap diambil dari `reason` di `flow.json`, bukan ditulis model.

## Dua mode (`TRIAGE_AI_MODE`)

| Mode | Panggilan per pasien | Isi |
|---|---|---|
| `single` (bawaan) | 1 | Semua kandidat, 1 potongan literatur per kandidat |
| `per_candidate` | 3 sampai 6 | Hanya kandidat pendek: anggota klaster yang dipilih + 2 skor teratas `RuleEngine`, 3 potongan per kandidat, dijalankan paralel |

`per_candidate` adalah cara yang terbukti berhasil di Gemma4 4B, tapi memakan kuota 3 sampai 6 kali lipat. Dengan batas sekitar 10 RPM, itu hanya 2 pasien per menit. Bandingkan keduanya di uji pengguna lewat log.

## Fallback

`meta.engine = "rules"` dan `meta.fallback = true`, dengan `meta.reason`:

| reason | Artinya |
|---|---|
| `model_off` | Tidak ada API key, atau `TRIAGE_AI_PROVIDER=off` |
| `quota_local` | Batas lokal RPM/RPD tercapai, atau masih jeda 60 detik setelah 429 |
| `rate_limited` | Google menjawab 429 |
| `timeout` | Lewat `TRIAGE_AI_CALL_TIMEOUT_S` atau `TRIAGE_AI_DEADLINE_S` |
| `bad_response` | Kosong, diblokir, terpotong, atau bukan JSON yang diminta |
| `network`, `server_error`, `error` | Gangguan jaringan, 5xx (dicoba ulang 1 kali), atau galat lain |

`reason` berawalan `skipped:` artinya model memang tidak perlu dipanggil (tanda bahaya, tidak ada yang bisa dinilai). Itu bukan fallback.

`ScoreResult` dari `POST /triage/flows/{flow_id}/score` membawa `engine` (`ai` / `rules` / `model`) dan `fallback`. Kolom `engine` di tabel `screening` diisi dari engine yang benar-benar dipakai, bukan dari setelan.

## Cache dan pratinjau

- **Cache hasil:** hasil AI yang sukses disimpan di memori proses (maks. 2048 entri; `TRIAGE_AI_CACHE_TTL_S`, bawaan 24 jam, `0` = tanpa cache). Kuncinya: jalur + jawaban (tanpa teks obat dan waktu selesai). Simpan skrining dan halaman QR dengan jawaban yang sama memakai hasil yang sama tanpa panggilan Gemini baru. Fallback tidak pernah dicache.
- **Pratinjau:** `POST /triage/flows/{flow_id}/score?preview=true` selalu memakai `RuleEngine` (misalnya pop-up obat setelah langkah q6), jadi tidak memakai kuota model.

## Log uji pengguna

Satu baris JSON per penilaian, diawali `ai_call`, ke output server (di Railway: tab Logs, cari `ai_call`) atau ke file `TRIAGE_AI_LOG_PATH`. File di Railway hilang setiap deploy, jadi pakai output server. Isinya `request_id`, mode, model, versi prompt dan literatur, skor model, skor aturan untuk pembanding, kandidat pendek, catatan singkat model per penyakit, sumber yang dikutip, latensi, token, dan baris fakta (`TRIAGE_AI_LOG_FACTS`). Tidak pernah berisi nama, NIK, BPJS, koordinat, foto, atau teks bebas obat.

## Satu panggilan model per pasien

Frontend memanggil endpoint skor beberapa kali: di langkah obat (q6) untuk pop-up peringatan obat, di layar "Kak Tropi sedang menebak", lalu backend menghitung ulang saat screening disimpan.

- Langkah obat memanggil dengan `?preview=true`. Skornya dihitung dengan `RuleEngine`, tidak pernah dengan model.
- Hasil model untuk jawaban yang sama dipakai ulang selama `TRIAGE_AI_CACHE_TTL_S` (bawaan 24 jam), jadi halaman hasil, ringkasan QR yang dipindai petugas belakangan, dan simpan screening menampilkan perkiraan yang sama tanpa memanggil Gemini lagi. Teks obat dan waktu pengisian tidak ikut dicocokkan. Cache ada di memori: deploy ulang mengosongkannya. Hasil fallback tidak disimpan, supaya percobaan berikutnya tetap mencoba model.
- Kolom `engine` di tabel `screening` sekarang berisi engine yang benar-benar dipakai: `ai`, `rules`, atau `ai-fb:<alasan>` (misalnya `ai-fb:timeout`).

## Pengenalan obat (`/drugs`)

Teks bebas langkah obat (Q6) dibaca model menjadi golongan: `nsaid`, `antimotilitas`, `ccb_dhp`, `acei`, `statin`, `diuretik`, `antikoagulan` (serta `lain` dan `tidak_dikenal`, yang tidak memicu apa pun).

- Model **hanya menyebut golongan**. Pop-up dan teks peringatan tetap dari `advice.json`: sebuah aturan menyala kalau kata kuncinya cocok **atau** golongannya ditemukan (`"classes"` di aturan).
- Model hanya dipanggil kalau ada aturan yang masih bisa menyala untuk jawaban itu dan belum tertangkap kata kunci. Contoh: NSAID hanya relevan untuk keluhan demam (A); pasien dengan keluhan kulit tidak memicu panggilan.
- Kalau semua item adalah obat yang sudah dikenal (chip obat atau kata kunci), model tidak dipanggil. Teks yang sama di-cache.
- Berjalan paralel dengan penilaian skor, dan tidak bergantung pada `TRIAGE_SCORING_ENGINE`: aktif kalau ada API key dan `TRIAGE_AI_DRUGS_ENABLED=true` (bawaan).
- Gagal (timeout, kuota, JSON salah) = golongan kosong; aturan kata kunci tetap berjalan seperti sebelumnya.
- Log hanya berisi nama generik dan golongan, bukan tulisan asli pasien.
- `POST /api/v1/ai/drugs` untuk mencoba langsung.

Tiga aturan baru dari Referensi Medis (Tahap 4, Sub-Trigger 1B) sudah ada di `advice.json` dengan `"pending_dr": true`: Statin, Diuretik, dan Antikoagulan pada pasien demam. **Aturan ini tidak akan menyala** sampai DR menyetujui teksnya dan baris `pending_dr` dihapus.

## Literatur

Peringkat potongan dihitung offline dengan EmbeddingGemma 2 (`google/embeddinggemma-2`, teks saja, float32 di CPU, 768 dimensi, dinormalisasi). Saat runtime tidak ada model embedding; `literature.py` hanya membaca JSON.

```bash
cd backend
# 1. Cek dulu model paham bahasa Indonesia (sekali saja, butuh unduhan model ~1 GB)
PYTHONPATH=. uv run --with sentence-transformers --with torch --with pillow python scripts/embedding_probe.py \
    --chunks app/triage/ai/data/infection_chunks.jsonl
# 2. Bangun ulang indeks (method "embedding-v1")
PYTHONPATH=. uv run --with sentence-transformers --with torch --with pillow python scripts/build_literature.py \
    --flow infection --chunks app/triage/ai/data/infection_chunks.jsonl
```

- Query = teks opsi kuis (bagian negatif dipotong, lihat `retrieval_text`), prefiks `task: search result | query: `. Dokumen = kartu, prefiks `title: none | text: `.
- `pillow` wajib ikut dipasang walau model dipakai teks saja: prosesor EmbeddingGemma 2 mengimpornya.
- Kartu tanpa tag `[Penyakit · Bagian]` dilewati dan dilaporkan di stderr (`--keep-untagged` untuk menyertakan).
- `for_disease()` mengalikan skor kartu **Gejala** dan **Kriteria Diagnosis** dengan `SYMPTOM_BOOST` (1.3) dan menaruhnya lebih dulu di potongan bawaan. Atur nilainya dari hasil A/B.
- Judul lengkap dokumen 54 masih placeholder di `SOURCE_TITLES`. Jalur kronis belum punya literatur, jadi model menilai tanpa sumber.

### A/B: aturan vs AI tanpa RAG vs AI + RAG

Otomatis: `TRIAGE_AI_API_KEY=... python scripts/ab_literature.py [per_candidate]`.

Di Swagger (login superuser), kasus yang sama dijalankan tiga kali:

| Lengan | Endpoint | Setelan |
|---|---|---|
| Aturan | `POST /triage/flows/infection/score?preview=true` | (tidak memakai model) |
| AI tanpa RAG | `POST /api/v1/ai/score` | `TRIAGE_AI_SOURCES_PER_CANDIDATE_SINGLE=0` (mode `per_candidate`: `TRIAGE_AI_SOURCES_PER_CANDIDATE=0`), restart server |
| AI + RAG | `POST /api/v1/ai/score` | setelan bawaan |

Bandingkan `ranked`, `sources`, `latency_ms`, dan `fallback` per kasus. Pilih kasus yang membingungkan (mis. DBD vs chikungunya, amebiasis vs diare), bukan hanya yang aturannya sudah benar.

## Pengaturan lain

- `TRIAGE_AI_FLOWS`: jalur yang dinilai model, bawaan `infection,chronic`. Jalur lain selalu memakai aturan (`reason=skipped:flow_off`).
- `TRIAGE_AI_TEMPERATURE`: kosong = bawaan model. Google sangat menyarankan bawaan (1.0) untuk Gemini 3; nilai rendah bisa membuat model berputar-putar atau penalarannya menurun.
- Model diminta menilai 3 sampai 5 kandidat teratas, termasuk yang skornya rendah, supaya "Kemungkinan lain" terisi. Data diri pasien (usia, jenis kelamin) dikirim ke model tapi tidak ditampilkan sebagai alasan.

## Ganti model

Bawaan: `gemini-3.5-flash-lite`. Model ini sudah dicoba dengan key sungguhan pada 15 Okt 2026 dan menjawab sesuai skema. `gemini-3.6-flash` menjawab 503 (server sibuk) tiga kali berturut-turut. Untuk memakai Flash sebagai model utama, set `TRIAGE_AI_MODEL=gemini-3.6-flash` dan `TRIAGE_AI_FALLBACK_MODEL=gemini-3.5-flash-lite`. Saat Flash menjawab 503 atau 429, Flash-Lite dicoba sekali sebelum service jatuh ke aturan, dan log mencatat model mana yang menjawab.

Cara lain cukup lewat config: `TRIAGE_AI_MODEL`, atau `TRIAGE_AI_PROVIDER=openai_compat` + `TRIAGE_AI_BASE_URL=http://<server-gpu>:8000/v1` untuk Gemma4 di vLLM. Naikkan `PROMPT_VERSION` di `prompts.py` setiap kali prompt atau skema berubah.

## OpenRouter (Gemma 4 gratis)

Pindah dari Gemini ke OpenRouter cukup lewat `.env`, tanpa mengubah kode:

```bash
TRIAGE_AI_PROVIDER=openai_compat
TRIAGE_AI_BASE_URL=https://openrouter.ai/api/v1
TRIAGE_AI_MODEL=google/gemma-4-26b-a4b-it:free
TRIAGE_AI_API_KEY=sk-or-...
TRIAGE_AI_SCHEMA_IN_PROMPT=true
TRIAGE_AI_RPM_LIMIT=20
TRIAGE_AI_RPD_LIMIT=50
TRIAGE_AI_CALL_TIMEOUT_S=30
TRIAGE_AI_DEADLINE_S=40
```

- **Batas model `:free`:** 20 permintaan per menit, 50 per hari. Setelah akun pernah membeli minimal 10 kredit, batas harian naik jadi 1.000. Kuota ini dipakai bersama oleh skoring (1 panggilan per pasien di mode `single`) dan pengenalan obat (paling banyak 1 panggilan lagi). Set `TRIAGE_AI_DRUGS_ENABLED=false` kalau kuota harus hemat; pop-up obat tetap jalan lewat kata kunci.
- **Skema JSON tidak dijamin.** Endpoint gratisnya (Google AI Studio) menerima `response_format` tapi tidak mendukung `structured_outputs`. `TRIAGE_AI_SCHEMA_IN_PROMPT=true` menulis skema ke pesan sistem, dan balasan yang dibungkus ```json tetap terbaca. Validasi ID di engine tetap berjalan seperti biasa.
- **Fallback berbayar (opsional):** `TRIAGE_AI_FALLBACK_MODEL=google/gemma-4-26b-a4b-it` dikirim sebagai daftar `models` OpenRouter. Kalau versi gratis kena 429 atau error, OpenRouter mencoba versi berbayar dalam permintaan yang sama (kira-kira Rp20–30 per pasien, butuh saldo kredit).
- **404 "No endpoints found matching your data policy":** buka pengaturan privasi OpenRouter dan izinkan endpoint gratis.
- Uji dulu dengan `python scripts/ai_smoke.py single` memakai kunci OpenRouter.

## Privasi

Data boleh keluar server (keputusan tim). Dengan Gemini API atau OpenRouter, fakta pasien (teks pilihan, usia, jenis kelamin, provinsi; tanpa identitas) dikirim ke Google (lewat OpenRouter bila memakai OpenRouter). Menurut Google, data di kuota gratis dipakai untuk memperbaiki produknya dan bisa dibaca peninjau manusia. Sebutkan ini di teks persetujuan dan di klaim deck.
