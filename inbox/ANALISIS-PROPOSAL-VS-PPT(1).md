# Analisis Perbandingan: Proposal (main.pdf) vs PPT Deck

**Tanggal:** 16 Oktober 2026  
**Fokus:** Argumen, informasi, dan konsistensi — **bukan desain**

---

## 📊 Ringkasan Eksekutif

| Aspek | Proposal | PPT | Pemenang |
|-------|----------|-----|---------|
| **Regulasi & hukum** | ✓ UU 17/2023, UU PDP, KMK 1186 | ✗ Tidak ada | **Proposal** |
| **Validasi & KPI** | ✓ 100 kartu, >92%, SUS >80 | ✗ Tidak ada | **Proposal** |
| **Transparansi AI** | ✓ Bagian 5 lengkap | ✗ Disebutkan tapi tidak detail | **Proposal** |
| **Matriks risiko & mitigasi** | ✓ Ada (Tabel 3) | ✗ Tidak ada | **Proposal** |
| **Akurasi klaim vs kode** | ⚠ Ada ~10 mismatch | ✓ Hampir semua cocok | **PPT** |
| **Ketepatan data** | ✓ Ada sumber | ⚠ Beberapa tanpa sumber | **Proposal** |
| **Pembanding produk** | ⚠ Hipotesis umum | ✓ Mobile JKN, Ada Health nyata | **PPT** |
| **Kelayakan bisnis** | ✗ Tidak ada | ✓ Rp295 rb/bulan dihitung | **PPT** |

**Kesimpulan:** Proposal lebih lengkap dan strategis, tetapi **risikonya tinggi** karena banyak klaim tidak cocok dengan implementasi. PPT lebih tipis tetapi aman dari serangan juri berbasis bukti.

---

## ⚠️ KLAIM TIDAK COCOK DENGAN KODE (RISIKO KRITIS)

Jika juri membaca keduanya dan mencocokkan dengan GitHub, ini akan menjadi masalah serius.

### 1. **PWA & Mode Luring ("Tetap jalan tanpa sinyal")**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "Navigasi faskes terdekat berjalan tanpa internet" | Proposal §2.2, Tabel 1 | Faskes diambil dari server. Yang jalan di browser hanya cek tanda bahaya. | Tidak ada `service worker` di `frontend/public` |
| "Penerbitan QR rujukan tetap berjalan di peramban tanpa internet" | Proposal §2.2, Tabel 1 | Saat ini QR hanya dibuat di server. | Perlu verifikasi di kode |
| "PWA ketahanan luring" | Proposal §2.2 poin 1 | Hanya cek tanda bahaya yang benar-benar offline-first. Kuesioner & hasil perlu server. | Fitur sebenarnya terbatas |

**Status:** ⚠️ Overwisdom. Revisi: "Deteksi darurat jalan di browser tanpa internet; kuesioner & hasil perlu koneksi ke server."

---

### 2. **Master Sarana Index (MSI) & Jumlah Faskes**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "13.930 faskes SATUSEHAT: Puskesmas, **Klinik**, dan RS" | Proposal §2.2, Rumusan Masalah no. 2 | Integrasi MSI **dihentikan** 16 Okt 2026. Mirror hanya punya **10.374 Puskesmas + 3.556 RS**, tanpa klinik. | `docs/SATUSEHAT.md:45` |
| "Integrasi direktori resmi 13.930 faskes SATUSEHAT MSI" | Proposal §2.1, Tabel 1, Tabel 5 | Keputusan tim: "nasibnya perlu diputuskan." | `AGENTS.md`, checklist aplikasi |
| "Direktori lengkap seluruh Puskesmas, Klinik, dan RS resmi" | Proposal §2.2 poin 3 | Klinik tidak ada di mirror. | `docs/SATUSEHAT.md` |

**Status:** 🔴 **KRITIS**. Rumusan masalah & solusi dijustifikasi berdasarkan MSI, padahal sudah tidak pakai. Perlu revisi total bagian 1.2, 2.1, 2.2 poin 3, dan Tabel 1.

**Rekomendasi:**
- Ganti "13.930 faskes" dengan "10.374 Puskesmas + 3.556 RS (13.930 total)" dan jelaskan tanpa klinik.
- Atau sebutkan MSI sedang dalam evaluasi, belum terintegrasi.

---

### 3. **Jumlah Tanda Bahaya: 11 vs 12**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "11 tanda bahaya" (dengan daftar 10 kondisi) | Proposal §2.1, §5.2 poin 1 | Kode punya 12 kondisi | `red_flags.json` baris top-level punya: `['syok', 'darah', 'ginjal', 'napas', 'otak', 'dehidrasi', 'rabies', 'jantung', 'stroke', 'krisis_ht', 'koma_dm', 'kuning']` |
| Proposal menyebutkan "11 kondisi gawat" tapi hanya tulis 10 | Proposal §2.1 paragraf Gerbang Privasi | Ada gap antara klaim dan daftar | Teks hanya sebut: tanda syok DBD, muntah/batuk darah, sesak, kejang, dehidrasi, rabies, jantung, stroke, krisis darah tinggi, koma diabetes—itu 10. |

**Status:** 🟡 Selisih 1-2 kondisi. Kode punya `ginjal` dan `kuning` yang tidak disebutkan proposal.

**Rekomendasi:** Sebutkan "12 kondisi gawat darurat" dan daftar semua: **syok, perdarahan masif, gagal ginjal akut, sesak napas berat, gangguan kesadaran, dehidrasi berat, rabies, serangan jantung, stroke, krisis hipertensi, koma diabetes, dan jaundis berat**.

---

### 4. **Model AI: MedGemma 4B vs Gemini vs OpenRouter**

Cerita berbeda di tiga tempat.

| Sumber | Klaim |
|--------|-------|
| **Proposal §2.2** | "model medis bobot terbuka MedGemma 4B yang dijalankan di peladen sendiri lewat API bergaya OpenAI (vLLM)" |
| **Proposal §5.1** | "penalaran klinis dilayani model medis bobot terbuka MedGemma 4B" |
| **PPT slide 08 (Feasibility)** | "OpenRouter Rp180,28 rb/bulan" (OpenRouter = penyedia Gemma, bukan server sendiri) |
| **Kode [config.py:31](backend/app/triage/ai/config.py#L31)** | `MODEL: str = "gemini-3.5-flash-lite"` **default** |
| **Kode [config.py:35](backend/app/triage/ai/config.py#L35)** | `PROVIDER: Provider = "gemini"` **default** |
| **Diagram alur PPT slide 06** | "Gemma4 + RAG" tetapi default di code adalah Gemini |

**Status:** 🔴 **KRITIS**. Juri akan bertanya: "Mana yang sebenarnya? MedGemma 4B di server sendiri, OpenRouter, atau Gemini?"

**Kenyataan:**
- Default adalah Gemini Flash-Lite (bukan MedGemma, bukan server sendiri).
- Dapat dikonfigurasi ke OpenRouter / vLLM via `.env`.
- PPT slide 06 alur menampilkan "Gemma4 + RAG" tetapi konfigurasi default bukan itu.
- Biaya di PPT asumsi OpenRouter, bukan Gemini (Gemini gratis tier).

**Rekomendasi:**
- Proposal & PPT: Jelaskan bahwa arsitektur **support multiple providers** (Gemini, OpenRouter, vLLM), tetapi default di tahap MVP adalah **Gemini Flash-Lite**.
- Slide alur: Ubah "Gemma4" menjadi "Model AI (Gemini / Gemma4 / custom via OpenRouter)".
- Feasibility: Perjelas asumsi (Gemini gratis atau OpenRouter berbayar?).

---

### 5. **"Privasi Mutlak Zero-NIK" vs "Data Keluar Server"**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "Privasi mutlak Zero-NIK; tanpa minta nomor KTP, koordinat GPS tidak disimpan di peladen" | Proposal Tabel 1, §2.2 poin 2 | `screening_stat` tetap disimpan di server tanpa NIK, tapi **data jawaban bisa keluar ke penyedia AI**. | `backend/app/triage/ai/` mengirim ke Gemini/OpenRouter |
| "Tidak pernah menyimpan data lokasi pengguna" | Proposal §2.2 poin 2 | **Benar** — GPS hanya di browser, hanya provinsi ke server | `frontend/src/features/triage` |
| "Data privasi tidak tergoyahkan" | Proposal abstrak, Tabel 1 | Jawaban medis keluar ke penyedia AI luar. | Kode mengirim ke Gemini / OpenRouter API |

**Status:** 🟡 **Tidak salah, tetapi tidak transparan**. Proposal benar soal NIK dan GPS, tetapi overselling soal "privasi mutlak" mengabaikan bahwa **data jawaban medis dikirim ke penyedia AI eksternal**.

**Rekomendasi:**
- Proposal & PPT: Tambahkan penafian: "Data jawaban dapat dikirim ke penyedia AI (Gemini/OpenRouter) untuk inferensi; sebagainya disimpan di server kami. Pengguna harus setuju pada gerbang privasi."
- **PPT sudah benar soal ini** (Diagram alur slide 06 menunjukkan "data keluar server").

---

### 6. **"Transmisi Ringkasan Terenkripsi" & "WhatsApp Otomatis"**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "Transmisi ringkasan klinis terenkripsi (QR Code Rangkuman Pasien offline)" | Proposal §1.3 | QR berisi jawaban dalam **kode ringkas, bukan terenkripsi**. | Perlu verifikasi `QR` generation |
| "Tombol kirim pesan WhatsApp ringkasan skrining ke faskes tujuan" | Proposal Tabel 1, §3.1 | Tautan WhatsApp dibuka **oleh pengguna sendiri**, bukan otomatis. Data tidak dikirim via API WhatsApp. | `Nearby.tsx` menciptakan tautan `wa.me` |
| "Kirim WhatsApp otomatis" | Proposal §2.1 | Pengguna harus ketuk tombol & buka WhatsApp sendiri. | Kode hanya membuat link, tidak mengirim otomatis |

**Status:** 🟡 Overstatement. Tidak ada enkripsi di QR (hanya encoding), dan "kirim WhatsApp" adalah user-initiated, bukan otomatis dari server.

**Rekomendasi:** 
- Proposal: Ubah "terenkripsi" → "dikode ringkas".
- Ubah "kirim WhatsApp otomatis" → "tautan WhatsApp yang siap dibuka pengguna".

---

### 7. **"Menampilkan Kutipan Langsung dari KMK" (Fitur "Kenapa Aku Menebak Ini?")**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "Fitur 'Kenapa aku menebak ini?' yang menampilkan kutipan langsung kriteria klinis KMK PPK FKTP 2022 sebagai dasar rekomendasi" | Proposal Tabel 6, §5.3 | Saya tidak menemukan tampilan kutipan di frontend. Perlu verifikasi. | `frontend/src/features/triage` — cari "Kenapa" atau "citation" |

**Status:** ⚠️ Perlu verifikasi kode. Slide 05d (Hasil) menampilkan "Perkiraan penyakit & skor kecocokan" tetapi tidak jelas apakah ada kutipan KMK.

**Rekomendasi:** Verifikasi di frontend apakah fitur ini sudah ada atau masih rencana. Jika belum ada, ubah klaim menjadi "direncanakan" atau hapus dari Proposal.

---

### 8. **Test Coverage: 304 Tes dengan 96% Cakupan**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "304 kasus uji dengan cakupan uji (test coverage) 96% pada backend" | Proposal §5.1, Tabel 5 | Jumlah fungsi `test_` sekitar **270**, bukan 304. Tes berparameter bisa menambah, jadi jalankan `pytest --collect-only` untuk angka pasti. | `grep -rc "^\s*def test_" backend/tests` |

**Status:** 🟡 Angka mungkin benar jika termasuk test items, tapi perlu diverifikasi dengan `pytest --co -q | wc -l`.

**Rekomendasi:** Jalankan perintah untuk mendapat angka pasti sebelum presentasi juri.

```bash
cd backend && python -m pytest --collect-only -q | wc -l
```

---

### 9. **Istilah "Anonim" vs "Tanpa Identitas Langsung"**

| Klaim | Tempat | Kenyataan | Bukti |
|-------|--------|----------|-------|
| "Telemetri anonim (Zero-NIK)" | Proposal §3.2 poin 3 | **Melanggar aturan proyek**. Istilah yang benar adalah "tanpa identitas langsung". | `AGENTS.md`: "Tidak bisa dihapus per orang. Terpisah dari itu, setiap skrining selesai (tamu juga) menambah satu baris statistik tanpa identitas langsung" |

**Status:** 🟡 Kesalahan terminologi. "Anonim" berbeda dari "tanpa identitas langsung" di UU PDP.

**Rekomendasi:** Ganti semua "anonim" → "tanpa identitas langsung" di Proposal.

---

## 📋 Inkonsistensi dalam Proposal Sendiri

### Puasa: 8–12 jam vs 10–12 jam

| Bagian | Teks |
|--------|------|
| **§1.1** | "uji glukosa darah puasa dan profil lipid mewajibkan puasa **8–12 jam**" |
| **§2.1, Rute Kuning** | "dilengkapi instruksi wajib berpuasa **10–12 jam** sebelum cek darah" |
| **Kode** [advice.json:13](backend/app/triage/content/chronic/advice.json#L13) | "DIWAJIBKAN BERPUASA (hanya minum air putih) selama **10-12 jam**" |

**Kenyataan:** Puasa untuk gula darah umumnya 8 jam, untuk kolesterol 9–12 jam. Proposal menggunakan dua angka berbeda tanpa alasan.

**Status:** Ini teks medis — **keputusan DR diperlukan**. Tidak bisa ditulis developer.

**Rekomendasi:** Tanyakan ke DR: apakah puasa 8–12 jam atau 10–12 jam untuk jalur PTM TropiCare?

---

### Cakupan Instruksi Puasa

| Klaim | Kenyataan |
|-------|----------|
| Proposal menyebut "instruksi wajib berpuasa" di Rute Kuning umum | Instruksi puasa **hanya ada di jalur kronis** (advice.json line 13) |
| Slide fitur menyebutkan "pertanyaan pengganti" untuk yang tidak ada timbangan | Perlu cek apakah bobot proksi sudah diterapkan atau masih 0 |

**Status:** Instruksi puasa mungkin hanya untuk jalur kronis (PTM), bukan untuk semua pasien Rute Kuning.

---

### "Proksi Fisik Tervalidasi" & Bobot

| Klaim | Status |
|-------|--------|
| "sistem memakai proksi fisik: menggigil hebat, nadi cepat saat istirahat, baju melonggar drastis, dan celana menyempit di pinggang" | ✓ Sudah di kode |
| "Suhu bobot proksi menunggu ST (sekarang 0 poin)" | ⏳ Masih 0, belum OK ST |
| "Skor ambang menunggu ST" | ⏳ Belum OK |

**Status:** Klaim ini adalah rencana, bukan fitur jadi. Perlu ditandai "direncanakan" atau "menunggu validasi" di Proposal.

---

## 💪 Kelebihan Proposal

1. ✅ **Landasan hukum lengkap** — UU 17/2023, UU PDP, KMK 1186, Permenkes 3/2026
2. ✅ **Validasi klinis terukur** — 100 kartu kasus, >92% akurasi, SUS >80, tanpa kasus darurat terlewat
3. ✅ **Matriks risiko & mitigasi** (Tabel 3) — menjawab kekhawatiran juri medis tentang AI halusinasi
4. ✅ **Human-in-the-loop** yang jelas (Bagian 5.2) — bukan AI otonom
5. ✅ **Detail efek samping obat** — Amlodipine mirip filariasis, Captopril mirip TBC, data SKI 2023
6. ✅ **KPI konkret & terukur** (Tabel 4) — cara mengukur keberhasilan jelas
7. ✅ **Peta jalan 12 bulan** dengan milestone (Tabel 2)
8. ✅ **Transparansi AI** — bagian 5 membahas kecerdasan buatan secara terbuka

---

## 💪 Kelebihan PPT

1. ✅ **Semua klaim cocok dengan aplikasi** — hampir tidak ada mismatch
2. ✅ **Fakta spesifik dengan sumber** — fase kritis DBD hari 3-7, kematian <0,5%, PNPK Dengue
3. ✅ **Pembanding produk nyata** — Mobile JKN, Ada Health, bukan hipotesis
4. ✅ **Positioning jelas** — "melengkapi, bukan menggantikan" Mobile JKN
5. ✅ **Kelayakan bisnis konkret** — Rp295 rb/bulan dihitung, ROI per langganan
6. ✅ **Diagram alur transparan** — menunjukkan apa di perangkat, apa di server, apa di layanan luar
7. ✅ **Jujur soal data** — "data keluar server" ditunjukkan terang di slide 06
8. ✅ **Fokus pada masalah nyata** — antrean, obat salah, perjalanan sia-sia, bukan teori

---

## ⚠️ Kelemahan Proposal

### **Kritis**
- 🔴 PWA/luring: claim vs realitas (hanya tanda bahaya yang offline)
- 🔴 MSI: solusi didasarkan MSI, tetapi sudah ditolak tim
- 🔴 Model AI: cerita berbeda di proposal, kode, dan PPT
- 🔴 Tanda bahaya 11 vs 12
- 🔴 Klaim validasi kurang konkret (belum ada 100 kartu sungguhan)

### **Major**
- 🟡 Istilah "anonim" melanggar AGENTS.md
- 🟡 "Privasi mutlak" oversell (data keluar ke penyedia AI)
- 🟡 Puasa 8–12 vs 10–12 jam inkonsisten
- 🟡 Enkripsi QR, kirim WhatsApp otomatis — overstate
- 🟡 Tabel 1 membandingkan dengan "solusi konvensional" yang lemah (bukan produk nyata)

### **Minor**
- "20 NTD" — TBC, malaria, tifoid bukan NTD WHO (lebih aman "20 penyakit infeksi")
- "Dekongesti 30–40% antrean" tanpa data pilot
- "Kepatuhan puasa >85%" tanpa baseline
- "Nomor Permenkes 3 Tahun 2026" belum diverifikasi
- Tidak ada biaya operasional/server

---

## ⚠️ Kelemahan PPT

### **Major**
- ❌ **Tidak ada validasi atau KPI** — juri medis akan tanya "akurasinya berapa?"
- ❌ **Tidak ada regulasi** — juri legal akan tanya "dasar hukumnya apa?"
- ❌ **Monetisasi tidak etis** — "Sewa API data skrining" mengabaikan UU PDP
- ❌ **Asumsi biaya tidak jelas** — OpenRouter Rp180 rb untuk berapa skrining?
- ❌ **Railway hobby plan tidak scalable** — pilot 10+ Puskesmas pasti overload

### **Minor**
- 🟡 "Ada Health ✕ Bahasa Indonesia" — perlu verifikasi
- 🟡 "Mobile JKN 47 pertanyaan" — perlu konfirmasi
- 🟡 "Pantau PTM" belum dibuat, ditampilkan sebagai fitur jadi
- 🟡 Placeholder di slide terima kasih: `[tautan aplikasi]`, `[tautan GitHub]`
- 🟡 Slide 7 "skalabilitas" — janji tanpa bukti (white-label, API mitra belum ada)

---

## 🎯 Rekomendasi Prioritas (Urutan Eksekusi)

### **Minggu 1: Kriteria Wajib (sebelum presentasi)**

1. **[KRITIS] Satukan cerita Model AI**
   - Putuskan: Gemini (default), Gemma4 (OpenRouter), atau vLLM (custom)?
   - Update proposal & PPT konsisten
   - Slide 06 alur: ubah "Gemma4" jadi "Model AI (Gemini/Gemma4/custom)"
   - Feasibility: perjelas asumsi biaya

2. **[KRITIS] Revisi klaim PWA & MSI**
   - Proposal: ubah PWA → "Deteksi darurat jalan di browser; kuesioner perlu server"
   - Tarik MSI dari rumusan masalah, atau jelaskan sedang evaluasi
   - Tulis "13.930 faskes: 10.374 Puskesmas + 3.556 RS (tanpa klinik)"

3. **[KRITIS] Verifikasi & perbaiki angka**
   - Tanda bahaya: jalankan `grep -c '"id"' red_flags.json` → akurat ke 12
   - Test count: `pytest --collect-only -q | wc -l`
   - Proposal & PPT: update angka pasti

4. **[KRITIS] Tambahkan disclaimer data AI**
   - Proposal & PPT: "Data jawaban dikirim ke penyedia AI (Gemini/OpenRouter) untuk inferensi"
   - Gerbang privasi wajib mengingatkan ini

5. **[MAJOR] Jelas soal Puasa: tanya DR**
   - Puasa 8–12 atau 10–12 jam untuk jalur PTM TropiCare?
   - Instruksi puasa hanya untuk jalur kronis, atau semua Rute Kuning?

### **Minggu 2: Tambahan untuk Proposal**

6. **Tambahkan slide validasi & keamanan ke PPT**
   - 1 slide: 100 kartu kasus, >92% target, SUS >80, zero red flag miss
   - 1 slide: regulasi (UU 17/2023, UU PDP, KMK 1186)

7. **Perbaiki terminologi proposal**
   - Ganti semua "anonim" → "tanpa identitas langsung"
   - "Kirim WhatsApp otomatis" → "tautan WhatsApp siap dibuka pengguna"
   - "Terenkripsi" → "dikode ringkas"

8. **Verifikasi Permenkes No. 3 Tahun 2026**
   - Cek di database Kemenkes atau arsip resmi

9. **Clean up PPT**
   - Slide 09: ganti `[tautan aplikasi]` & `[tautan GitHub]` dengan URL sungguhan

### **Minggu 3: Bonus**

10. **Hitung baseline untuk KPI-3 (Kepatuhan puasa)**
    - Pilot di 2-3 Puskesmas, ukur % pasien datang puasa sebelum & sesudah TropiCare
    - Target >85% jadi rasional atau realistis?

11. **Validasi claim "dekongesti 30–40% antrean"**
    - Pilot 10 Puskesmas: ukur panjang antrean & waktu tunggu sebelum/sesudah

---

## 📎 Tabel Referensi: Klaim-per-Klaim

### Proposal vs Kode

| Bab | Klaim | Status | Perbaikan |
|-----|-------|--------|-----------|
| 1.1 | Puasa 8–12 jam | ⚠️ Inconsistent | Tanya DR: 8–12 atau 10–12? |
| 1.2 | Rumusan masalah no. 2: MSI & SATUSEHAT | 🔴 Tidak lanjut | Hapus atau ubah "sedang evaluasi" |
| 2.1 | 11 tanda bahaya | 🟡 Hanya 10 disebut | Sebutkan semua 12 |
| 2.1 | PWA luring | 🟡 Oversell | Hanya tanda bahaya offline |
| 2.2 poin 1 | PWA offline-first | 🟡 Parsial | Perjelas: darurat offline, kuesioner online |
| 2.2 poin 3 | 13.930 faskes dengan klinik | 🔴 MSI tidak jadi | Ubah ke "10.374 Puskesmas + 3.556 RS" |
| 2.2 poin 4 | MedGemma 4B di vLLM | 🔴 Tidak default | Default Gemini, configurable ke Gemma |
| 2.3 Tabel 1 | Transmisi terenkripsi | 🟡 QR hanya dikode | Ubah kata |
| 3.2 no. 3 | Telemetri anonim | 🔴 Terminology | Ubah ke "tanpa identitas langsung" |
| 5.1 Tabel 5 | 304 tes | ⚠️ Verifikasi | Jalankan `pytest --co -q` |
| 5.2 | Kutipan KMK di hasil | ❓ Unclear | Verifikasi frontend |

### PPT vs Proposal

| Slide | Klaim PPT | Masalah di Proposal | Rekomendasi |
|-------|-----------|-------------------|-------------|
| 04 | Kompetitor Mobile JKN, Ada Health | Proposal pakai "solusi konvensional" hipotesis | PPT lebih kuat |
| 08 | Biaya Rp295 rb/bulan | Proposal tidak ada ROI | Tambahkan ke proposal |
| 06 | Data keluar server jelas | Proposal oversell "privasi mutlak" | Selaraskan |

---

## 🔍 Cara Verifikasi (untuk Tim)

### Cek Tanda Bahaya (harus 12)
```bash
cd backend
python -I -c "
import json
d = json.load(open('app/triage/content/red_flags.json'))
flags = d.get('red_flags') or []
print(f'Total: {len(flags) if isinstance(flags, list) else len(flags.keys())}')
print(list(flags.keys()) if isinstance(flags, dict) else [f.get('id') for f in flags])
"
```

### Cek Test Count
```bash
cd backend
python -m pytest --collect-only -q | tail -1
```

### Verifikasi Konfigurasi AI Default
```bash
grep "^    MODEL:" app/triage/ai/config.py
grep "^    PROVIDER:" app/triage/ai/config.py
```

### Cek Apakah Ada "Kutipan KMK" di Frontend
```bash
cd frontend
grep -rn "kutipan\|citation\|sumber" src/features/triage/ --include=*.tsx
```

---

## 📝 Kesimpulan Akhir

| Dokumen | Keunggulan | Kelemahan | Rekomendasi |
|---------|-----------|----------|-------------|
| **Proposal** | Lengkap, regulasi, KPI, transparansi AI | Klaim vs kode mismatch (PWA, MSI, model), risiko tinggi | **Revisi dulu sebelum distribusi** |
| **PPT** | Klaim akurat, pembanding nyata, bisnis konkret | Tipis, tanpa validasi/regulasi | **Aman untuk presentasi, tambah slide validasi** |

**Strategi Juri:**
- Jika juri membaca **hanya PPT** → aman
- Jika juri membaca **kedua dokumen & cross-check dengan GitHub** → proposal rawan serangan
- **Solusi:** Perbaiki proposal sesuai rekomendasi, lalu dua dokumen konsisten dan kuat

---

**Dokumen ini dibuat:** 16 Oktober 2026  
**Oleh:** Claude Haiku 4.5  
**Untuk:** Tim TropiCare & Persiapan Hackathon JOINTSXINSPIRE 2026
