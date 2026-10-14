# Alur Data dan Format per Tahap

Acuan ST untuk mengembangkan skor dan model: data apa yang masuk di setiap tahap, formatnya, apa yang dihitung, dan apa yang harus dikeluarkan model. Isi medis (kriteria, rute, teks) ada di [Acuan-Medis.md](Acuan-Medis.md). Dokumen ini hanya membahas data.

Sumber kebenaran di kode:

| Apa | File |
| --- | --- |
| Format jawaban (`Answers`) dan hasil (`ScoreResult`) | `backend/app/triage/schemas.py` |
| Skor aturan, fitur model, kerangka `ModelEngine` | `backend/app/triage/scoring.py` |
| Rute, peringatan, rangkuman (aturan tetap) | `backend/app/triage/advice.py` |
| Analisis foto (kerangka) | `backend/app/triage/vision.py` |
| ID pilihan dan bobot | `backend/app/triage/content/<flow>/flow.json`, `weights.json` |

Kalau dokumen ini berbeda dengan kode, kode yang benar. Perbarui dokumen ini.

---

## 1. Gambaran alur

```
Browser                                     Server (milik sendiri)
───────                                     ──────────────────────
GET /api/v1/triage/flows/{flow_id}  ───────▶ pertanyaan + ID pilihan (tanpa bobot)
        │
Data diri → Tanda bahaya ──[ada]──▶ layar MERAH (di browser, tanpa server)
        │ [tidak ada]
Keluhan → Gejala → Ekologi → Obat → Pengukuran → Peta nyeri → Foto
        │                                          │
        │                 POST /triage/photo/analyze (opsional, foto tidak disimpan)
        ▼
POST /triage/flows/{flow_id}/score  ───────▶ Answers
                                              │
                                              ▼
                                   Engine.score()  ← bagian ST
                                   (RuleEngine sekarang, ModelEngine nanti)
                                              │  ScoreBreakdown
                                              ▼
                                   advice.build_result()  ← aturan tetap
                                   (rute, kenaikan rute, peringatan, rangkuman)
                                              │
        ◀──────────────────────── ScoreResult ┘

Simpan (hanya jika pasien setuju):
POST /triage/screenings {flow_id, answers, consent: true} → tabel screening
GET  /triage/screenings (superuser) → data untuk analisis ST
```

- `flow_id`: `infection` (jalur infeksi) atau `chronic` (jalur kronis/PTM).
- Endpoint `score` tidak menyimpan apa pun. Penyimpanan hanya lewat `screenings` dengan `consent: true`.

---

## 2. Format per tahap

Semua jawaban dikirim sekaligus di akhir, sebagai satu objek `Answers`. Tabel ini memetakan setiap tahap ke field-nya.

| Langkah (`step`) | Tahap | Field `Answers` | Tipe dan rentang | Nilai | Kapan diisi |
| --- | --- | --- | --- | --- | --- |
| `who` | Data diri | `who` | string | `self` · `child` · `elder` · `other` | selalu |
| | | `age` | int 0–120, tahun | | selalu |
| | | `sex` | `"L"` / `"P"` | | selalu |
| | | `pregnant` | bool / null | | hanya `sex = "P"` dan `age ≥ 10`; selain itu `null` |
| `q1` | Tanda bahaya | `red_flags` | list ID, maks 20 | ID di §3.1, atau `["none"]` | selalu, minimal satu |
| `q2` | Keluhan utama | `complaint` | string ≤ 4 | infeksi `A`–`E`; kronis `F`–`H` atau `none` | selalu |
| `q3` | Pola gejala | `pattern` | string ≤ 20 | ID pola klaster itu, atau `none` | jika klaster punya pertanyaan pola |
| `q4` | Gejala penyerta | `companion` | list ID | ID penyerta klaster itu, atau `["none"]` | jika klaster punya pertanyaan penyerta (lihat §3.3) |
| `q5` | Ekologi / faktor risiko | `eco` | list ID | ID di §3.4, atau `["none"]` | selalu |
| `q6` | Riwayat obat | `drugs` | teks bebas ≤ 500 karakter | contoh `"Paracetamol, Ibuprofen"` | opsional, boleh `""` |
| `q7` | Tanda vital | `temp` | float 34–43 °C, 1 desimal | | infeksi; `null` jika `no_thermo` |
| | | `no_thermo` | bool | | infeksi |
| | | `bp_sys`, `bp_dia` | int 50–300 / 30–200 mmHg | | kronis; `null` jika `no_bp` |
| | | `no_bp` | bool | | kronis |
| | | `glucose` | float 10–1000 mg/dL | | kronis, opsional |
| | | `vital_proxy` | list ID | §3.5 | hanya jika `no_thermo` atau `no_bp`; selain itu `[]` |
| `q8` | Antropometri | `height_cm`, `weight_kg` | float 0–300 / 0–500 | | opsional |
| | | `waist_cm` | float 0–250 | | kronis, opsional |
| | | `nutrition_proxy` | `longgar` · `gemuk` · `normal` / null | | jika IMT tidak bisa dihitung |
| `q9` | Peta nyeri | `body` | list ID wilayah | §3.6 | infeksi saja; boleh `[]` |
| | | `pain` | int 0–10 / null | wajah 0, 2, 4, 6, 8, 10 | hanya jika `body` tidak kosong |
| `q10` | Foto | `findings` | list ID temuan | §3.7, atau `["none"]` | opsional |
| — | Lokasi | `province` | nama provinsi ≤ 64 | | ⏳ belum dikirim front end |
| — | Waktu | `taken_at` | ISO 8601 + offset | `2026-10-13T15:04:00+08:00` | saat kuis selesai |

**Catatan format**

- **Kosong ≠ tidak.** `null` berarti tidak ditanya atau tidak diisi. `"none"` berarti pasien menjawab "tidak ada". Bedakan keduanya di model.
- **Langkah yang dilewati.** `q3` dan `q4` tidak muncul jika klaster tidak punya pertanyaannya. Contoh: klaster `C` dan `E` tidak punya penyerta, jadi `companion` = `[]`.
- **Pilihan yang dibatasi usia** (`sth`: 1–12 tahun; `mr`: anak < 18 tahun) tidak dinilai bila usia tidak cocok, walau terkirim.
- **Server memvalidasi rentang.** Nilai di luar rentang ditolak (HTTP 422).

---

## 3. Daftar ID

ID dipakai bersama oleh FE, BE, dan skor. **Jangan mengganti nama ID tanpa mengganti ketiganya**, karena nama fitur model ikut berubah.

### 3.1 Tanda bahaya (kedua jalur)

`syok` · `darah` · `ginjal` · `napas` · `otak` · `dehidrasi` · `rabies` · `jantung` · `stroke` · `krisis_ht` · `koma_dm` · `none`

Ini tidak pernah masuk model. Satu ID selain `none` → rute MERAH.

### 3.2 Klaster, pola, dan perkiraan

ID pola sama dengan ID penyakit yang ditunjuknya (kecuali `none`).

| Jalur | Klaster | ID pola | Perkiraan yang ikut di klaster (`members`) |
| --- | --- | --- | --- |
| infeksi | `A` Demam | `dbd` `chik` `malaria` `lepto` `skisto` | dbd, malaria, chik, lepto, skisto |
| infeksi | `B` Napas | `ispa` `tbc` | ispa, tbc |
| infeksi | `C` Perut | `diare` `amoeba` `tifoid` `hepa` `sth` | diare, tifoid, amoeba, hepa, sth |
| infeksi | `D` Kulit | `scabies` `tinea` `campak` `varicella` `kusta` `frambusia` | sama |
| infeksi | `E` Bengkak | `filaria` | filaria |
| kronis | `F` Gula & Saraf | `dm` `neuropati` | dm, neuropati |
| kronis | `G` Tekanan & Kepala | `hipertensi` (→ hipertensi + dislipidemia), `angina` | hipertensi, angina, dislipidemia |
| kronis | `H` Sendi | `gout` | gout |

`rabies` ada di daftar penyakit tetapi tidak diskor (`scored: false`).

### 3.3 Gejala penyerta

| Klaster | ID → perkiraan | Catatan |
| --- | --- | --- |
| `A` | `dbd` → dbd · `chik` → chik · `malaria` → malaria | |
| `B` | `bb` → tbc · `kms` → tbc | |
| `D` | `mata` · `sesak` · `nanah` | Hanya jika `pattern = varicella`. Tidak memberi poin; menaikkan rute ke minimal KUNING. |

### 3.4 Ekologi / faktor risiko

- Infeksi: `timur` · `danau` · `banjir` · `padat` · `kontak` · `mr` (anak saja) · `none`
- Kronis: `keturunan` · `rokok` · `metabolik` · `none`

### 3.5 Proksi tanda vital

- Infeksi (`temp`): `menggigil` · `nadi` · `none`
- Kronis (`bp`): `nadi` · `tengkuk` · `none`

### 3.6 Wilayah tubuh (infeksi)

`head` · `chest` · `ruq` (perut kanan atas) · `luq` (ulu hati) · `low` (perut tengah/bawah) · `arm_r` · `arm_l` · `wrist_r` · `wrist_l` · `thigh_r` · `thigh_l` · `calf_r` · `calf_l` · `ankle_r` · `ankle_l`

### 3.7 Temuan foto

| Jalur | ID → perkiraan |
| --- | --- |
| infeksi | `ruam` → campak, dbd · `lenting` → varicella · `bercak` → kusta · `borok` → frambusia · `mata` → hepa, lepto · `none` |
| kronis | `borok` → dm · `tofus` → gout · `leher` → dm · `none` |

`borok` menunjuk penyakit berbeda di tiap jalur.

---

## 4. Nilai turunan

Dihitung di server dari `Answers`. Model boleh memakai nilai ini atau nilai mentahnya.

| Nilai | Rumus / aturan | Kode |
| --- | --- | --- |
| IMT | `weight_kg / (height_cm/100)²`, hanya jika tinggi 50–230 cm dan berat 3–250 kg; selain itu `null` | `scoring.bmi()` |
| Status gizi | IMT < 18,5 → `kurus`; ≥ 27 → `obes`; selain itu `normal`. Tanpa IMT: `longgar` → `kurus`, `gemuk` → `obes`, `normal` → `normal` | `scoring.nutrition()` |
| Anak | `age < 18` | `scoring.is_child()` |
| Demam terukur | `temp ≥ 38,0` dan `no_thermo = false` | `weights.fever.min_temp` |
| Obat berisiko | Kata kunci di `drugs` (huruf kecil, cocok sebagian) + syarat keluhan/pola. Hanya untuk peringatan, tidak memberi poin | `advice.drug_flags()` |

---

## 5. Vektor fitur untuk model

`scoring.features(answers, content)` mengubah `Answers` menjadi `dict[str, float]`. Pakai ini sebagai masukan model terlatih, supaya nama fitur sama dengan data yang tersimpan.

| Nama fitur | Isi | Hilang |
| --- | --- | --- |
| `age` | usia, tahun | NaN |
| `sex_p` | 1 = perempuan, 0 = laki-laki | NaN |
| `pregnant` | 1 / 0 | NaN (tidak ditanya) |
| `temp` | °C | NaN (tidak punya termometer / tidak diisi) |
| `bmi` | IMT | NaN |
| `pain` | 0–10 | NaN |
| `bp_sys`, `bp_dia` | mmHg | NaN |
| `glucose` | mg/dL | NaN |
| `waist` | cm | NaN |
| `complaint_{klaster}` | one-hot, mis. `complaint_A` | 0 |
| `pattern_{id}` | one-hot, mis. `pattern_dbd` | 0 |
| `companion_{klaster}_{id}` | mis. `companion_B_bb` | 0 |
| `eco_{id}` | mis. `eco_danau` | 0 |
| `proxy_{id}` | proksi gizi, mis. `proxy_longgar` | 0 |
| `vital_{vital}_{id}` | mis. `vital_temp_nadi` | 0 |
| `body_{id}` | mis. `body_calf_r` | 0 |
| `finding_{id}` | mis. `finding_ruam` | 0 |

Belum ada di fitur: `who`, `drugs`, `province`. Tambahkan kalau model membutuhkannya. **Setelah model dilatih, jangan ubah nama fitur.**

---

## 6. Keluaran yang harus diberikan model

Setiap engine (aturan atau model) mengimplementasikan `ScoringEngine.score(answers, content) -> ScoreBreakdown`:

```python
ScoreBreakdown(
    scores={"dbd": 75.0, "malaria": 30.0, "chik": 10.0, ...},  # setiap ID di content.scored_diseases
    reasons={"dbd": ["Demam pelana kuda ...", "Suhu terukur 38.6 °C (demam)"], ...},
    ranked=rank(scores, weights.softmax_temperature),
)
```

- **`scores`**: satu angka per ID perkiraan di `diseases.json` (selain `rabies`). Skalanya sama dengan skor aturan (kira-kira 0–100). Kalau skala model berbeda, ubah ambang di `weights.json` (lihat §7).
- **`reasons`**: kalimat untuk "Kenapa aku menebak ini?". Enam teratas ditampilkan. Untuk model: kontribusi fitur terbesar, atau kutipan dari RAG. Teks yang dilihat pasien perlu OK DR.
- **`ranked`**: hasil `rank()`, yaitu softmax atas skor positif. `pct` di layar = bagian softmax × 100.
- Tidak boleh ada nama penyakit di luar `diseases.json`. Model memilih dari ID yang ada, bukan teks bebas.

### Yang bukan tugas model (aturan tetap di `advice.py`)

Tetap berjalan apa pun engine-nya. Model tidak boleh menimpanya.

1. Tanda bahaya → MERAH.
2. Skor tertinggi < `low_score_threshold` → "belum dapat ditentukan" + KUNING.
3. Rute = rute penyakit teratas (`diseases.json`).
4. HIJAU → KUNING jika `temp ≥ 39,5` atau `bp_sys > 160`.
5. Tanda Varicella berat (`min_route`) → minimal KUNING.
6. Peringatan obat, Chikungunya kronis, malaria + obesitas, dan rangkuman.

---

## 7. Parameter skor aturan (`weights.json`)

Milik ST. Angka saat ini di jalur infeksi:

| Parameter | Nilai | Arti |
| --- | --- | --- |
| `complaint_base` | 10 | Poin untuk setiap anggota klaster yang dipilih |
| `pattern` | 40 | Pola gejala yang cocok |
| `companion` | 20 | Per gejala penyerta |
| `finding` | 25 | Per temuan foto |
| `eco` | per ID | Mis. `danau` → skisto 25; `padat` → tbc 8, scabies 12, tinea 8, hepa 8 |
| `province` | `{}` | ⏳ kosong |
| `fever` | ≥ 38,0 °C → +5 ke 7 penyakit; varicella +2 tanpa alasan | |
| `nutrition` | kurus → tbc 10, kusta 6, sth 10; obes → malaria 5 | |
| `body` | sendi pergelangan → chik 10 (18 jika nyeri ≥ 6); aturan per wilayah; tungkai satu sisi → filaria 20 | |
| `softmax_temperature` | 20 | Makin besar, persentase makin rata |
| `candidate_min_share` | 0,05 | Batas "N kemungkinan" di gelembung maskot |
| `max_display_pct` | 97 | Persentase tertinggi yang ditampilkan |
| `low_score_threshold` | 30 | Di bawah ini → "belum dapat ditentukan" |
| `high_fever_upgrade` | 39,5 | Aturan tetap (DR), bukan bobot |
| `bp_upgrade_above` | 160 | Aturan tetap, bukan bobot |
| `chik_chronic_warning` | nyeri ≥ 7, skor chik ≥ 20 | Syarat peringatan |
| `malaria_obese_warning_min_score` | 40 | Syarat peringatan |

**Dinilai 0 poin sampai ST menetapkan bobot:** proksi suhu/tensi (`vital_proxy`), `bp_sys`/`bp_dia`, `glucose`, `waist_cm`, `pregnant`, `province`, faktor risiko kronis (`chronic/weights.json` `eco: {}`). Jalur kronis masih menyalin angka jalur infeksi. Skor CVD (`scoring.cvd_risk()`) masih mengembalikan `None`.

---

## 8. MedGemma + RAG: titik sambung

Pembagian tugas antara MedGemma dan skor aturan adalah keputusan ST. Bagian ini hanya mencatat batasannya.

**Batasan**

- Model berjalan di server sendiri. Tidak ada API pihak luar, tidak ada data yang keluar.
- Sumber RAG hanya literatur yang disetujui DR. Catat daftar sumbernya (judul, versi, tanggal).
- Hasil harus bisa dijelaskan: setiap skor punya `reasons`.
- Kalau model mati atau lambat, aplikasi harus tetap memberi hasil. Contoh: kembali ke `RuleEngine`. Tentukan batas waktunya bersama BE.

**Tempat menyambung**

| Kebutuhan | Tempat | Masukan | Keluaran |
| --- | --- | --- | --- |
| Skor teks | `ModelEngine.score()` di `scoring.py`; aktifkan dengan `TRIAGE_SCORING_ENGINE=model` | `Answers` (atau `features()`, atau `advice.summary()` sebagai teks) | `ScoreBreakdown` (§6) |
| Analisis foto | kelas baru di `vision.py`; aktifkan dengan `TRIAGE_PHOTO_ANALYZER` | gambar (jpeg/png/webp/heic, ≤ 8 MB) | list ID temuan (§3.7) |

`advice.summary()` menghasilkan teks rangkuman tanpa identitas. Teks ini bisa dipakai sebagai masukan MedGemma bila ST memilih masukan berupa teks.

⚠️ `POST /triage/photo/analyze` belum menerima `flow_id`. Padahal ID temuan berbeda per jalur (`mata` hanya infeksi; `tofus`, `leher` hanya kronis; `borok` di keduanya). Minta BE menambahkannya sebelum model foto dipasang.

**Privasi foto:** jangan tulis ke disk, log, atau database. Perbarui teks persetujuan di layar foto saat foto mulai dikirim ke server.

---

## 9. Data yang tersimpan

Tabel `screening`, hanya jika pasien setuju:

| Kolom | Isi |
| --- | --- |
| `id` | UUID |
| `flow_id` | `infection` / `chronic` |
| `answers` | JSON `Answers`, tanpa field yang bernilai bawaan (`exclude_defaults`) |
| `route` | `green` · `yellow` · `special` · `red` |
| `unknown` | true jika "belum dapat ditentukan" |
| `top_disease`, `top_score` | perkiraan teratas dan skornya |
| `engine` | `rules` / `model`, untuk membandingkan engine |
| `created_at` | UTC |

- Tidak ada nama, NIK, nomor BPJS, foto, atau tautan ke akun pengguna.
- Unduh lewat `GET /api/v1/triage/screenings?skip=0&limit=100` (akun superuser).
- Uji coba memakai kartu kasus, bukan data kesehatan asli peserta. Data di tabel ini berasal dari peserta yang mengisi kartu kasus.

---

## 10. Contoh

**Masukan (jalur infeksi)**

```json
{
  "who": "self",
  "age": 22,
  "sex": "L",
  "pregnant": null,
  "red_flags": ["none"],
  "complaint": "A",
  "pattern": "malaria",
  "companion": ["malaria"],
  "eco": ["timur"],
  "drugs": "Paracetamol",
  "temp": null,
  "no_thermo": true,
  "vital_proxy": ["menggigil"],
  "height_cm": null,
  "weight_kg": null,
  "nutrition_proxy": "longgar",
  "body": ["head"],
  "pain": 4,
  "findings": ["none"],
  "taken_at": "2026-10-14T09:30:00+09:00"
}
```

**Masukan (jalur kronis, tanpa keluhan)**

```json
{
  "who": "elder",
  "age": 58,
  "sex": "P",
  "pregnant": false,
  "red_flags": ["none"],
  "complaint": "none",
  "eco": ["keturunan", "metabolik"],
  "drugs": "Amlodipine",
  "no_bp": false,
  "bp_sys": 150,
  "bp_dia": 95,
  "glucose": 180,
  "height_cm": 155,
  "weight_kg": 70,
  "waist_cm": 92,
  "findings": ["leher"]
}
```

Keluaran lengkap: jalankan backend, lalu coba di `http://localhost:8000/docs` → `POST /triage/flows/{flow_id}/score`.

---

## 11. Usulan: format kartu kasus untuk evaluasi

Usulan supaya kartu kasus DR bisa langsung dipakai untuk menguji skor. Format akhir disepakati DR dan ST.

```json
{
  "id": "KK-001",
  "flow_id": "infection",
  "vignette": "Pemuda 22 tahun pulang KKN di Papua 2 minggu lalu ...",
  "answers": { "...": "objek Answers seperti §10" },
  "expected": {
    "route": "red",
    "top": "malaria",
    "acceptable_top3": ["malaria", "dbd"]
  },
  "author": "DR",
  "approved": true
}
```

Ukuran yang bisa dipakai:

- **Ketepatan rute.**
- **Rute terlalu rendah** (undertriage), misalnya harusnya MERAH/KUNING tetapi keluar HIJAU. Ini yang paling berbahaya; laporkan terpisah.
- **Perkiraan teratas benar** (top-1) dan **masuk 3 besar** (top-3).
- **Proporsi "belum dapat ditentukan"**.

Bandingkan `RuleEngine` dan `ModelEngine` dengan kartu kasus yang sama.
