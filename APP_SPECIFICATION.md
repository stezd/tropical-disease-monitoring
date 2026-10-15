# SPESIFIKASI DAN ARSITEKTUR APLIKASI TROPICARE
*Dokumen Rujukan Teknis, Medis, dan Konseptual*
*Status Implementasi: Branch `master` per Oktober 2026*

---

## 1. Ringkasan Eksekutif (Executive Summary)

**TropiCare** adalah platform triase mandiri dan pemandu rujukan pra-hospital berbasis web (*Progressive Web App*) yang dirancang untuk memilah kondisi kesehatan masyarakat Indonesia secara cepat, aman, dan mendidik.

Aplikasi ini memadukan **Rule Engine deterministik** (untuk keselamatan pasien gawat darurat dan kepatuhan pedoman dasar) dengan **Medical Large Language Model yang diperkuat Retrieval-Augmented Generation (RAG)** berbasis korpus resmi Kementerian Kesehatan RI. TropiCare menjembatani kesenjangan akses faskes, mencegah keterlambatan penanganan kondisi gawat darurat, menekan bahaya swamedikasi yang keliru, dan mengoptimalkan alur rujukan berjenjang ke Fasilitas Kesehatan Tingkat Pertama (FKTP / Puskesmas) maupun Instalasi Gawat Darurat (IGD).

> **Prinsip Utama:** TropiCare adalah alat **skrining mandiri (*screening/triage*)**, bukan penegak diagnosis medis definitif. Pasien tidak pernah diberikan label "diagnosis", melainkan "perkiraan kecocokan" yang wajib dikonfirmasi oleh dokter.

---

## 2. Masalah Nyata yang Diselesaikan

1. **Penumpukan Antrean di Puskesmas untuk Kasus Ringan:** Banyak pasien dengan keluhan ringan (Tingkat Kemampuan 4A SKDI) memadati Puskesmas, padahal cukup ditangani melalui swaperawatan teredukasi di rumah.
2. **Keterlambatan Pasien Gawat Darurat (Red Flags):** Pasien dengan tanda syok atau komplikasi fatal kerap terlambat menuju IGD karena tidak menyadari bahaya atau bingung mencari fasilitas gawat darurat.
3. **Pembatalan Uji Laboratorium Akibat Tidak Puasa:** Banyak pasien lansia/PTM yang datang ke Puskesmas untuk cek gula darah puasa (GDP) atau profil lipid terpaksa pulang karena sudah sarapan (kurang edukasi prasyarat puasa 8–12 jam).
4. **Bahaya Swamedikasi Obat Bebas:** 
   - Konsumsi NSAID (Ibuprofen, Asam Mefenamat, Aspirin) saat demam memicu perdarahan cerna fatal pada fase kritis DBD.
   - Konsumsi antimotilitas (Loperamide) pada disentri/amebiasis memicu *toxic megacolon*.
   - Efek samping obat rutin sering merancukan gejala (Amlodipine memicu bengkak kaki mirip filariasis, Captopril memicu batuk kering mirip TBC).
5. **Salah Rujukan di Wilayah Pedalaman/Kepulauan:** Warga menempuh perjalanan jauh ke faskes yang ternyata tidak menyediakan obat program nasional (OAT TBC, MDT Kusta, atau Praziquantel).
6. **Ketiadaan Alat Ukur Medis di Rumah Tangga:** Sebagian besar masyarakat tidak memiliki termometer, timbangan presisi, atau tensimeter di rumah.

---

## 3. Cakupan Penyakit dan Alur Klinis

TropiCare menyediakan dua jalur skrining utama:

### A. Jalur Infeksi Akut (20 Penyakit Tropis Endemis & Terabaikan)
Mengelompokkan keluhan ke dalam 5 klaster sindromik utama:
1. **Klaster Demam & Badan:** DBD, Malaria, Demam Tifoid, Leptospirosis, Chikungunya, Schistosomiasis.
2. **Klaster Napas & Batuk:** ISPA / Rinitis Akut, Faringitis / Tonsilitis, Tuberkulosis (TBC), Pertusis.
3. **Klaster Pencernaan:** Diare Akut / Gastroenteritis, Amebiasis / Disentri Amoeba, Hepatitis A, Infeksi Cacing (STH: Ascaris/Trichuris/Ancylostoma).
4. **Klaster Kulit & Bercak:** Varicella (Cacar Air), Morbili (Campak), Skabies (Kudis), Kusta / Lepra, Tinea (Kadas/Kurap), Cutaneous Larva Migrans (CLM).
5. **Klaster Bengkak & Kelanjar:** Filariasis (Kaki Gajah).

### B. Jalur Kronis (Penyakit Tidak Menular / PTM)
Skrining faktor risiko penyakit metabolik dan degeneratif jangka panjang:
- **Klaster Gula & Saraf:** Risiko Diabetes Melitus Tipe 2, neuropati perifer.
- **Klaster Tekanan & Kepala:** Hipertensi, risiko penyakit serebrovaskular.
- **Klaster Sendi & Nyeri:** Gout Arthritis (asam urat), Osteoarthritis.
- **Kalkulator Risiko Kardiovaskular (CVD):** Stratifikasi risiko kardiovaskular 10 tahun (WHO SEAR-B non-laboratorium chart) berbasis umur, jenis kelamin, tekanan darah, dan status merokok.

---

## 4. Arsitektur 4 Lapisan Klinis (The 4-Layer Architecture)

```
[ Pengguna Membuka Web ]
        │
        ▼
[ GERBANG PRIVASI (Consent Tick) ] ── (Wajib centang persetujuan sebelum pertanyaan)
        │
        ▼
[ LAPISAN 1: Demografi & Emergency Check (Red Flags) ]
        ├─► Ada Tanda Bahaya? ──► [ BYPASS LANGSUNG KE RUTE MERAH (IGD / 119) ]
        │                          (100% Client-Side di Browser, Tanpa Server)
        ▼
[ LAPISAN 2: Klaster Keluhan & Peta Ekologi One Health ]
        ├─► Pilih Keluhan Utama (Demam / Napas / Cerna / Kulit / Bengkak / PTM)
        └─► Riwayat Risiko: Endemis Papua/NTT, Banjir, Hutan, Kontak TBC
        │
        ▼
[ LAPISAN 3: Farmakovigilans & Proksi Fisik ]
        ├─► Deteksi Obat: Peringatan NSAID, Antimotilitas, Captopril, Amlodipine
        ├─► Proksi Suhu: Isi °C atau jawab menggigil/keringat dingin/nadi istirahat
        ├─► Proksi Gizi: Tinggi/berat badan atau proksi pakaian (melonggar/gemuk)
        └─► Peta Nyeri Tubuh Interaktif (SVG Body Map) & Skala Nyeri 0–10
        │
        ▼
[ LAPISAN 4: Mesin Inferensi AI (Evidence-Grounded RAG) ]
        ├─► Aturan Pengaman Deterministik (Suhu ≥ 39.5°C, Sistolik > 160 mmHg)
        ├─► Retrieval BM25 atas Dokumen PPK FKTP Kemenkes 2022
        ├─► Inferensi Medical LLM (MedGemma / DeepSeek / Gemini)
        │
        ▼
[ HASIL TRIASE & NAVIGASI RUJUKAN (4 RUTE) ]
        ├─► MERAH: IGD Terdekat + Panggilan 119
        ├─► KUNING KHUSUS: Poli Khusus Faskes (DOTS TBC, Kusta MDT, Rabies Center)
        ├─► KUNING: Puskesmas Terdekat + Arahan Puasa Pra-Lab
        └─► HIJAU: Perawatan Mandiri Terpandu di Rumah
```

---

## 5. Spesifikasi Teknis & Teknologi (Tech Stack)

### A. Frontend
- **Framework:** React 19, TypeScript, Vite.
- **Routing:** TanStack Router.
- **Styling & UI:** Tailwind CSS, shadcn/ui component library, CSS custom TropiCek.
- **Peta Nyeri Tubuh:** SVG Interactive Body Map (responsif sentuhan per area organ/sendi).
- **Skala Nyeri:** Wong-Baker Faces Scale vertikal (nilai 0–10 tanpa default awal agar tidak memancing bias).
- **Enkripsi & QR:** Generator QR lokal (`qrcode-generator`) untuk membuat QR Rangkuman Pasien *offline*.
- **Client API:** Tergenerasi otomatis dari OpenAPI (`openapi-ts`).

### B. Backend
- **Framework:** FastAPI (Python 3.14).
- **ORM / Database:** SQLModel (SQLAlchemy) + PostgreSQL 18.
- **Arsitektur:** Ports & Adapters (Hexagonal Architecture):
  - `api/routes/`: Endpoint HTTP handler.
  - `application/use_cases/`: Orkestrasi proses bisnis triase (`score_flow.py`).
  - `domain/`: Kebijakan bisnis murni (`route_policy.py`, `warnings.py`, `narration.py`).
  - `adapters/`: Akses data (JSON disk repository, SQLModel database).
  - `composition/`: Dependency Injection root (`triage_container.py`).
- **Migrations:** Alembic.
- **Validasi Data:** Pydantic v2.

### C. Mesin Inferensi AI (Scoring Engines)
Sistem memiliki arsitektur mesin penilaian ganda yang dapat dikonfigurasi via environment variable (`TRIAGE_SCORING_ENGINE`):
1. **RuleEngine (`rules`):** Engine berbasis bobot aturan klinis deterministik (`weights.json`). Cepat, tanpa latensi eksternal, dan menjadi *fallback* absolut jika model AI gagal/timeout.
2. **AIEngine (`ai`):**
   - **Provider:** Mendukung Google Gemini API langsung dan protokol **OpenAI-Compatible** (vLLM lokal, 9router, OpenCode Go).
   - **Model Teruji:** `MedGemma` (target utama on-premise), `deepseek-v4.1-flash`, `gemini-3.8-flash`.
   - **Retrieval (RAG):** Menggunakan mesin temu balik BM25 sparse retrieval atas korpus teks resmi KMK No. HK.01.07/MENKES/1186/2022 (Panduan Praktik Klinis Dokter di FKTP).
   - **Prompt Contract:** Mematuhi format input `TextRequest` (fakta $F_1 \dots F_n$, sumber literatur $S_1 \dots S_n$) dan menghasilkan `TextOutput` berformat **Strict JSON Schema**.
   - **Toleransi Gateway:** Parser parser AI (`_json_object`) mentolerir berbagai pembungkusan gateway (fenced markdown ```json, bare array, trailing prose agentik) dan mengonversi otomatis field alias `candidate` $\rightarrow$ `id`.
   - **Safety Guards:**
     - Suhu $\ge 39,5^\circ\text{C}$ atau tekanan sistolik $>160$ mmHg otomatis menaikkan rute minimal ke KUNING.
     - Jika skor tertinggi $<30\%$ atau selisih ambigu $\rightarrow$ klasifikasi "belum dapat ditentukan" dan dirujuk ke KUNING.

---

## 6. Integrasi SATUSEHAT & Sistem Rujukan

Berdasarkan dokumen arsitektur `docs/SATUSEHAT.md` dan analisis privasi:

### A. Pola Integrasi: Local Mirror (Bukan Runtime Proxy)
TropiCare **tidak melakukan push resource FHIR Pasien/Encounter** ke SATUSEHAT karena:
1. TropiCare bersifat **anonim tanpa NIK** (kepatuhan UU PDP No. 27/2022).
2. TropiCare adalah **skrining mandiri non-diagnosis**, sehingga mengunggah diagnosis ICD-10 tanpa tatap muka dokter berisiko malpraktik hukum.

Solusi: Menggunakan **Master Sarana Index (MSI) Tier 1 Local Mirror**:
- Database lokal memuat **13.930 faskes terverifikasi** (10.374 Puskesmas + 3.556 Rumah Sakit) seluruh Indonesia.
- Sinkronisasi batch terjadwal via CLI (`scripts/sync_facilities.py`).

### B. Temuan Koordinat & Solusi Navigasi Presisi
- **Temuan Lapangan (15 Okt 2026):** Koordinat di registri MSI memiliki pergeseran bias rata-rata hingga **3 km** dari lokasi fisik sebenarnya (misal Puskesmas Gang Sehat), dan beberapa baris memiliki koordinat yang melompat ke provinsi lain.
- **Solusi Rekayasa TropiCare:**
  - Koordinat faskes hanya digunakan untuk **mengurutkan jarak terdekat (haversine)**.
  - Tombol **"Rute"** pada aplikasi secara sengaja membuka navigasi Google Maps berbasis **Nama Faskes Resmi + Kota** (`${facilityName}, ${cityName}`), bukan pin koordinat mentah. Google Maps yang menyelesaikan pencarian ke lokasi gedung faskes sebenarnya.

### C. One-Tap Referral WhatsApp
- Daftar faskes terdekat memprioritaskan fasilitas yang memiliki kontak WhatsApp aktif di urutan teratas (maksimal 5 faskes).
- Tombol WhatsApp membuka tautan `wa.me` dengan **pesan yang terisi otomatis (*pre-filled*) berupa teks Rangkuman Skrining Pasien** (`ScoreResult.summary`, $\pm$ 450–570 karakter).
- Teks rangkuman berisi dugaan kondisi, rute, keluhan utama, tanda vital/proksi, riwayat obat, dan usulan lab pemeriksaan, **tanpa memuat NIK, nama lengkap, atau foto**. Nakes faskes langsung mengetahui kondisi pasien tanpa wawancara ulang.

### D. QR Code Rangkuman Pasien
- Pada rute rujukan (Kuning/Kuning Khusus/Merah), sistem menghasilkan QR code terenkripsi.
- Isi QR = tautan aplikasi ringkas + parameter hash `#d=...`.
- Dokter di Puskesmas cukup memindai QR code ini; halaman `/ringkasan` dipecahkan **100% lokal di browser dokter tanpa mengirim data ke server**, menampilkan kondisi pasien dan saran penanganan siap cetak/injeksi.

---

## 7. Kebijakan Privasi & Mediko-Legal (Must Not Break)

1. **Prinsip Non-Diagnosis:** Aplikasi tidak boleh menggunakan kata "diagnosis". Gunakan kata **"skrining"** atau **"perkiraan"**.
2. **Kerahasiaan Data (No NIK / No BPJS):** Aplikasi tidak pernah meminta NIK, nomor kartu BPJS, atau tanggal lahir presisi.
3. **Privasi Koordinat:** Koordinat lintang/bujur pengguna hanya diproses di memori browser lokal untuk menentukan provinsi dan mengurutkan faskes terdekat; server hanya menerima nama provinsi tempat tinggal.
4. **Persetujuan Tindakan (*Privacy Consent Gate*):** Pasien wajib mencentang persetujuan privasi di awal kuesioner sebelum pertanyaan dimulai.
5. **Rute Merah Serius & Tenang:** Layar darurat Rute Merah bebas dari suara permainan, animasi ceria, atau maskot. Menampilkan tombol panggil 119 besar, nomor 119 dan 112 yang bisa disalin, panduan pertolongan pertama (DO \& DON'T), dan rute IGD terdekat.
6. **Keputusan Tim Foto:** Fitur unggah foto ruam/kulit telah **resmi dihapus per 15 Oktober 2026** demi perlindungan data biometrik/sensitif pasien dan kepatuhan regulasi.

---

## 8. Ringkasan Fitur Unggulan untuk Proposal Kompetisi

| Fitur Inovasi | Nilai Tambah Medis & Teknis |
|---|---|
| **Evidence-Grounded Medical LLM** | Inferensi didasarkan pada dokumen PPK FKTP Kemenkes 2022 via RAG, bukan halusinasi LLM bebas. |
| **Client-Side Emergency Override** | 11 tanda bahaya gawat darurat diuji langsung di browser tanpa ketergantungan sinyal internet atau server. |
| **Active Pharmacovigilance** | Peringatan otomatis bahaya obat NSAID (DBD), antimotilitas (disentri), Captopril (batuk), dan Amlodipine (edema). |
| **Non-Instrument Clinical Proxies** | Konversi proksi fisik (kelonggaran baju, menggigil, skala nyeri) bagi masyarakat tanpa alat ukur medis. |
| **SATUSEHAT MSI Directory Mirror** | Navigasi 13.930 Puskesmas & RS nasional dengan rute nama faskes presisi bebas bias koordinat. |
| **Instant WhatsApp Screening Summary** | Transmisi data skrining terstruktur ke WhatsApp faskes tujuan dalam satu sentuhan (*zero-retyping*). |
| **Zero-NIK Privacy Architecture** | Perlindungan privasi mutlak sesuai UU PDP No. 27/2022 tanpa menuntut identitas kependudukan. |
