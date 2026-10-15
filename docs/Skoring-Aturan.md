# Cara Kerja Skoring Tanpa AI (RuleEngine)

- **Untuk:** tim (BE, ST, DR). Penjelasan, bukan keputusan.
- **Kode:** `backend/app/triage/scoring.py` (`RuleEngine`). Kalau berbeda dengan dokumen ini, kode yang benar.
- **Bobot:** `backend/app/triage/content/<flow>/weights.json`. Perubahan bobot perlu OK ST.
- **Rute:** `backend/app/domain/route_policy.py` (`decide_route`)

## Ringkasan

Skoring aturan bekerja seperti kartu poin: setiap jawaban menambah poin ke penyakit tertentu, dan penyakit dengan poin tertinggi menjadi perkiraan utama. Semua angka ada di `weights.json`, jadi bisa diubah tanpa menyentuh kode. Rute rujukan tidak ditentukan mesin skoring, tetapi oleh aturan tetap yang sama untuk semua mesin.

## Kapan dipakai

Mesin skoring dipilih dengan setting `TRIAGE_SCORING_ENGINE` di `composition/triage_container.py`.

| Setting | Mesin | Keterangan |
| --- | --- | --- |
| `rules` (bawaan) | RuleEngine | Skoring aturan dengan bobot dari JSON |
| `ai` | MedGemma | Kalau gagal, RuleEngine yang menghitung (`engine="rules"`, `fallback=True`) |
| `model` | ModelEngine | Kerangka untuk model latih ST, belum diisi |

Pratinjau di tengah kuis (misalnya pop-up obat, `?preview=true`) selalu memakai RuleEngine supaya cepat dan tidak memanggil model.

## Sumber poin (jalur infeksi)

Pola gejala memberi poin terbesar (+40). Keluhan utama hanya +10, sehingga klaster saja tidak langsung menentukan perkiraan.

| Jawaban | Poin | Penerima |
| --- | --- | --- |
| Keluhan utama (klaster A–E) | +10 (`complaint_base`) | Semua anggota klaster, misalnya A = DBD, Malaria, Chik, Lepto, Skisto |
| Pola gejala (tahap 3) | +40 (`pattern`) | Penyakit yang ditunjuk opsi (ID opsi = ID penyakit, kecuali opsi punya `targets`) |
| Gejala penyerta, per centang | +20 (`companion`) | Penyakit target opsi |
| Peta ekologi | bervariasi (`eco`) | `banjir` → Lepto +20; `kontak` → TBC +20; `danau` → Skisto +25; `padat` → Scabies +12, TBC/Tinea/Hepa +8 |
| Suhu terukur ≥ 38,0 °C | +5 (`fever`) | DBD, Malaria, Chik, Lepto, Skisto, Tifoid, Campak; Varicella +2 tanpa alasan tampil |
| Gizi kurang (IMT < 18,5 atau proksi "pakaian longgar") | +10 / +6 | TBC dan STH +10; Kusta +6 |
| Obesitas (IMT ≥ 27 atau proksi) | +5 | Malaria |
| Nyeri pergelangan tangan/kaki | +10, atau +18 bila skala nyeri ≥ 6 | Chikungunya |
| Nyeri area lain | sesuai `body.rules` | Misalnya perut kanan atas → Hepatitis +20 |
| Nyeri di satu sisi tubuh saja | sesuai `body.asymmetry` | Diatur di weights.json |
| Provinsi | 0 | Tabel `province` masih kosong |

- Opsi yang dibatasi usia (`child_only`, `age_min`, `age_max`) hanya memberi poin kalau usia cocok. Usia kosong berarti opsi dianggap tidak terlihat.
- Proksi vital, tensi, gula darah, asam urat, kolesterol, dan lingkar perut belum memberi poin. Datanya tetap masuk rangkuman dan `features()`.
- Setiap tambahan poin dicatat sebagai `Contribution(penyakit, poin, alasan)`. `accumulate()` menjumlahkan poin per penyakit dan mengumpulkan alasan tanpa duplikat. Daftar alasan ini yang tampil di "Kenapa aku menebak ini?".

Jalur kronis memakai mesin yang sama dengan `chronic/weights.json`-nya sendiri.

## Dari poin ke persen

`rank()` mengambil penyakit dengan skor > 0, lalu menghitung softmax dengan suhu `softmax_temperature = 20`:

```text
persen_i = e^(skor_i / 20) / Σ e^(skor_j / 20)
```

| Nilai di layar | Aturan | Bobot |
| --- | --- | --- |
| Persen kecocokan | Hasil softmax; meteran maskot dibatasi maks. 97 % | `max_display_pct` |
| "N kemungkinan" | Jumlah penyakit dengan share ≥ 5 % | `candidate_min_share` |
| Kemungkinan lain | Peringkat 2 sampai 4 | — |

## Dari skor ke rute

Aturan dicek berurutan di `decide_route()`:

1. **Ada tanda bahaya** (termasuk gejala penyerta bertanda `red_flag`, misalnya mata sangat kuning saat demam) → **MERAH**.
2. **Skor teratas < 30** (`low_score_threshold`) → "belum dapat ditentukan", rute **KUNING**.
3. **Selain itu**, rute mengikuti `route` milik penyakit teratas di `diseases.json`. Kalau rutenya **HIJAU**, naik ke **KUNING** bila suhu ≥ 39,5 °C (`high_fever_upgrade`) atau sistolik > 160 mmHg (`bp_upgrade_above`).
4. **Tanda keparahan** pada opsi yang dipilih (`min_route`, misalnya Varicella dekat mata) bisa menaikkan rute lebih jauh.

## Contoh hitungan

Jawaban rekaan: keluhan demam (A), pola "DBD", gejala penyerta "DBD", suhu 38,5 °C, lingkungan padat.

| Penyakit | Rincian poin | Skor | Kecocokan |
| --- | --- | --- | --- |
| DBD | 10 + 40 + 20 + 5 | 75 | ≈ 74 % |
| Malaria, Chik, Lepto, Skisto | 10 + 5 | 15 masing-masing | ≈ 4 % masing-masing |
| Scabies | 12 (padat) | 12 | ≈ 3 % |
| TBC, Tinea, Hepatitis | 8 (padat) | 8 masing-masing | ≈ 3 % masing-masing |

Hanya DBD yang share-nya ≥ 5 %, jadi maskot menulis "1 kemungkinan". Skor 75 ≥ 30, jadi rute mengikuti rute DBD di content.

## Yang masih menunggu

- ⏳ Bobot provinsi endemis (DR + ST)
- ⏳ Bobot proksi vital, tensi, gula darah, asam urat, kolesterol, dan lingkar perut (ST)
- ⏳ Rumus skor CVD jalur kronis (`cvd_risk`, ST)
- ⏳ Model latih untuk `ModelEngine` (ST)
