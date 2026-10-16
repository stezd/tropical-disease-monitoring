# Rekomendasi Penyelarasan Strategi: Swasta vs. Nasional (TropiCare)

Dokumen ini menganalisis celah (*gap*) antara **Proposal Inovasi Hackathon** dan **Slide Presentasi (Pitch Deck)** TropiCare (khususnya Slide 11: *Skalabilitas* dan Slide 12: *Feasibility*), serta memberikan rekomendasi strategi yang paling realistis di hadapan juri.

---

## 1. Analisis Realitas: Mengapa Memilih Salah Satu Ekstrem Bermasalah?

### A. Jika Murni Swasta (Komersial B2B/B2C SaaS)
1. **Pasar Penyakit Tropis adalah *Market Failure*:**
   - 20 penyakit tropis (Kusta, Frambusia, Filariasis, Skistosomiasis, TBC) terkonsentrasi pada kelompok sosio-ekonomi menengah ke bawah dan wilayah 3T/rural.
   - Obat program eliminasi (OAT, MDT, Praziquantel) **hanya disediakan gratis oleh pemerintah di Puskesmas**, bukan klinik swasta komersial.
   - Pasien di segmen ini tidak memiliki daya beli untuk fitur berbayar seperti "Pantau PTM Rp15 rb/bulan".
2. **Kendala Pengadaan APBD/BLUD di Puskesmas:**
   - Di Slide 12 tertulis *Dasbor faskes untuk Puskesmas & klinik (~Rp250–400 rb/bulan)*.
   - Puskesmas adalah instansi pemerintah (UPTD Dinkes). Kepala Puskesmas **tidak dapat menggesek kartu kredit atau mentransfer kas operasional bulanan** ke startup luar tanpa mata anggaran resmi di DPA/RBA, proses lelang, atau penunjukan dari Dinas Kesehatan.
3. **Benturan Regulasi & Etika Data (Sewa API Rp15–40 jt/tahun):**
   - Proposal mengedepankan prinsip etis ketat: **Zero-NIK**, non-diagnosis, dan kepatuhan UU PDP No. 27/2022.
   - Menjual "Sewa API akses data skrining" rawan dicurigai sebagai komersialisasi data kesehatan masyarakat.

### B. Jika Murni Nasional (Kemenkes / Dinkes / APBN)
1. **Siklus Regulasi Sangat Panjang:**
   - Integrasi resmi ke ekosistem SATUSEHAT / SIMPUS membutuhkan *Regulatory Sandbox*, sertifikasi ISO 27001, audit interoperabilitas FHIR, dan birokrasi lintas direktorat yang memakan waktu 1–2 tahun.
2. **Kerentanan Keberlanjutan Proyek (*Hackathon Trap*):**
   - Juri bisnis kerap melontarkan kritik: *"Jika Kemenkes tidak mendanai atau proyek gagal lelang di Dinkes, bagaimana produk ini bertahan hidup?"*

---

## 2. Solusi Paling Realistis: Strategi Hibrida (*Dual-Track / B2B2G*)

Harmonisasi terbaik adalah **memisahkan jalur berdasarkan karakteristik masalah klinisnya**:

| Dimensi | Jalur Publik & Komunitas (Nasional / B2G / Hibah) | Jalur Layanan Mandiri & Faskes Pratama (B2B Swasta) |
| :--- | :--- | :--- |
| **Fokus Klinis** | 20 Penyakit Tropis, 11 Tanda Bahaya (*Red Flags*), Eliminasi NTD | Skrining Penyakit Tidak Menular (Hipertensi, Diabetes, Asam Urat, Obesitas) |
| **Target Pengguna** | Masyarakat rentan daerah endemis, kader Posyandu, warga 3T | Pasien umum perkotaan/suburban, lansia, klinik pratama swasta |
| **Model Akses** | **100% Gratis.** | **Freemium / B2B Subscription.** |
| **Sumber Finansial** | 1. Hibah riset / lembaga donor kesehatan global (Gates Foundation, NLR, Stop TB).<br>2. Alokasi BOK (Bantuan Operasional Kesehatan) Dinas Kesehatan daerah endemis. | 1. Modul efisiensi antrean & pra-triase loket untuk **Klinik Pratama Swasta** (~Rp250–400 rb/bln).<br>2. Fitur buku harian kesehatan mandiri (*self-monitoring* PTM). |
| **Peran Dasbor** | **Dasbor Surveilans Epidemiologi:** Statistik agregat spasial persebaran suspek (anonymized) untuk Dinkes. | **Dasbor Loket Faskes:** Pembaca QR triase cepat untuk memangkas waktu tunggu registrasi. |

---

## 3. Revisi Konkret pada Slide Presentasi

Agar pitch deck selaras dengan prinsip ilmiah dan kepatuhan di proposal, perbarui teks pada Slide 11 dan Slide 12 sebagai berikut:

### Perubahan Slide 11 (*Skalabilitas*)

| Bagian | Teks Awal di Slide | Teks Rekomendasi (Lebih Realistis & Etis) |
| :--- | :--- | :--- |
| **Jangkauan (Poin 1)** | Dasbor Puskesmas dan klinik | **Dasbor Pra-Triase Faskes:** Mengurai antrean pendaftaran di klinik mitra & Puskesmas pilot. |
| **Jangkauan (Poin 2)** | Surveilans wilayah untuk Dinkes dari statistik tanpa identitas... | **Peta Sinyal Dini Endemis:** Agregat tren suspek per kecamatan untuk respon cepat Dinas Kesehatan daerah. |
| **Jangkauan (Poin 3)** | White-label untuk LSM dan API untuk mitra | **Kemitraan Eliminasi Program:** Kolaborasi dengan NGO kesehatan (eliminasi TBC, Kusta, Kaki Gajah). |
| **Roadmap Bawah** | 1. Validasi $\rightarrow$ 2. Pilot klinik $\rightarrow$ 3. TropiCare Plus $\rightarrow$ 4. White-label $\rightarrow$ 5. API mitra | **1. Validasi Klinis $\rightarrow$ 2. Pilot Klinik & Posyandu $\rightarrow$ 3. Modul B2B Faskes $\rightarrow$ 4. Kemitraan Dinkes $\rightarrow$ 5. Sandbox Kemenkes** |

---

### Perubahan Slide 12 (*Feasibility / Kelayakan*)

Poin penting di slide ini adalah **menunjukkan efisiensi biaya infrastruktur**, namun modul monetisasinya perlu disesuaikan agar tidak melanggar etika privasi.

#### Sisi Kiri: Biaya Aplikasi (Tetap Pertahankan)
> Total biaya server sangat efisien: **~Rp295.000 / bulan** (Railway hobby plan Rp90 rb + inferensi AI efisien Rp180 rb + domain Rp25 rb).  
> *Insight:* Cukup **1 faskes mitra langganan (Rp400 rb)** untuk menutup seluruh biaya server bulanan aplikasi.

#### Sisi Kanan: Rekomendasi Modul Pendanaan / Monetisasi

1. **Kotak 1: Modul Loket Klinik Pratama (~Rp250–400 rb/bulan)**
   - *Target:* Klinik pratama swasta non-pemerintah.
   - *Value proposition:* Pemindai QR web untuk pra-triase otomatis pasien datang, memangkas antrean loket tanpa perlu investasi software rekam medis baru.
2. **Kotak 2: Kemitraan Program & Hibah Riset (Bukan "Sewa API")**
   - *Ganti label "Sewa API" menjadi:* **Hibah Program & CSR Kesehatan**.
   - *Deskripsi:* Kolaborasi pendanaan CSR farmasi / hibah filantropi eliminasi penyakit tropis terabaikan (NTD) untuk penyediaan server dan sosialisasi di daerah 3T.
3. **Kotak 3: Pendamping Skrining PTM (TropiCare Personal / B2C Opsional)**
   - *Target:* Pasien penyakit kronis keluarga (hipertensi/diabetes).
   - *Fitur:* Pencatatan riwayat tensi/gula darah mandiri dan pengingat kontrol rutin/puasa lab. Skrining dasar tetap 100% gratis.

---

## 4. Panduan Menjawab Pertanyaan Juri

* **Jika juri bertanya: "Ini proyek idealis Kemenkes atau startup bisnis komersial?"**
  > *"TropiCare menggunakan pendekatan **B2B2G bertahap**. Masalah penyakit tropis adalah tanggung jawab kesehatan masyarakat yang skrinning intinya harus gratis dan bermitra dengan Kemenkes/Dinkes. Namun, agar tidak mati menunggu birokrasi, keberlanjutan operasional TropiCare ditopang secara mandiri lewat layanan efisiensi pra-triase untuk klinik pratama swasta. Biaya operasional server kami yang hanya ~Rp300 ribu per bulan membuatnya sangat cepat mencapai titik impas (breakeven). Setelah matang di pilot faskes swasta, sistem kami siap masuk ke Regulatory Sandbox Kemenkes untuk skala nasional."*

* **Jika juri bertanya: "Bagaimana cara monetisasi data jika menganut Zero-NIK?"**
  > *"Kami **tidak menjual data pasien**. Model monetisasi kami adalah penyediaan perangkat lunak efisiensi alur kerja (B2B workflow tools) untuk klinik, serta kemitraan hibah program pemberantasan penyakit endemis. Data analitik epidemiologi hanya disajikan dalam bentuk agregat wilayah tanpa identitas langsung demi kepentingan surveilans kesehatan masyarakat daerah."*
