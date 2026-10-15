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
| `POST /api/v1/ai/score` | Lewat HTTP: skor, alasan, sumber, dan penanda fallback. |
| `GET /api/v1/ai/status` | Model, mode, pemakaian kuota lokal. Superuser saja. |

## Alur

1. `build_request()` (kontrak ST di `medgemma.py`) mengubah jawaban jadi fakta F1..Fn. Ada tanda bahaya: model tidak dipanggil.
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

`per_candidate` adalah cara yang terbukti berhasil di MedGemma 4B, tapi memakan kuota 3 sampai 6 kali lipat. Dengan batas sekitar 10 RPM, itu hanya 2 pasien per menit. Bandingkan keduanya di uji pengguna lewat log.

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

Saran untuk ST: kolom `engine` di tabel `screening` sekarang diisi `settings.TRIAGE_SCORING_ENGINE`. Kalau ingin data uji pengguna akurat, isi dari `meta.engine` dan `meta.reason` saat engine-nya `ai`.

## Log uji pengguna

Satu baris JSON per penilaian, ke logger `app.triage.ai` atau ke file `TRIAGE_AI_LOG_PATH`. Isinya `request_id`, mode, model, versi prompt dan literatur, skor model, skor aturan untuk pembanding, kandidat pendek, catatan singkat model per penyakit, sumber yang dikutip, latensi, token, dan baris fakta (`TRIAGE_AI_LOG_FACTS`). Tidak pernah berisi nama, NIK, BPJS, koordinat, foto, atau teks bebas obat.

## Literatur

```bash
python scripts/build_literature.py --flow infection \
    --chunks app/triage/ai/data/infection_chunks.jsonl
```

Pembangun sementara memakai BM25 per penyakit. Notebook Colab (EmbeddingGemma) bisa menggantikannya selama menulis format yang sama (lihat docstring `literature.py`); service tidak perlu diubah. Judul lengkap dokumen 54, 20, dan 57 masih perlu diisi di `SOURCE_TITLES` dan disetujui DR. Jalur kronis belum punya literatur, jadi model menilai tanpa sumber.

## Ganti model

Hanya config: `TRIAGE_AI_MODEL`, atau `TRIAGE_AI_PROVIDER=openai_compat` + `TRIAGE_AI_BASE_URL=http://<server-gpu>:8000/v1` untuk MedGemma di vLLM. Naikkan `PROMPT_VERSION` di `prompts.py` setiap kali prompt atau skema berubah.

## Privasi (perlu keputusan tim)

`AGENTS.md` menulis bahwa model berjalan di server sendiri dan tidak ada data keluar. Dengan Gemini API, fakta pasien (teks pilihan, usia, jenis kelamin, provinsi; tanpa identitas) dikirim ke Google. Menurut Google, data di kuota gratis dipakai untuk memperbaiki produknya dan bisa dibaca peninjau manusia. Ini perlu disebut di teks persetujuan dan di klaim deck, atau diganti ke `openai_compat` di server sendiri.
