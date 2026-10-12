# Rencana Kerja Hackathon TropiCek

**Tenggat luaran:** Jumat, 16 Oktober 2026, 23:50 WIB
**Tenggat internal:** Jumat, 16 Oktober 2026, **21:00 WIB** (sisa ±3 jam sebagai cadangan kalau unggahan gagal atau ada yang mendadak rusak)

**Luaran:** source code GitHub · prototipe (URL yang bisa dibuka) · proposal · pitch deck · video

| Kode         | Peran      |
| ------------ | ---------- |
| **FE** | Frontend   |
| **BE** | Backend    |
| **ST** | Statistika |
| **DR** | Dokter     |

---

## 1. Keputusan yang dipakai

### Teknologi

Repo memakai **Full Stack FastAPI Template**: FastAPI + PostgreSQL di backend, React + TypeScript di frontend. Fitur **registrasi, login, dan profil sudah tersedia** di template, jadi tidak perlu dibuat dari nol. File [TropiCek-Simulasi.html](TropiCek-Simulasi.html) menjadi acuan tampilan dan dipindahkan ke React, dengan koreksi dari bagian 7.

### Isi kuis berbentuk data

Pertanyaan, pilihan jawaban, dan bobot skor disimpan dalam file JSON di `backend/app/triage/content/`. Dengan begitu DR dan ST bisa mengubah isi tanpa menunggu FE mengubah kode. Ini kunci supaya keempat orang bisa bekerja paralel.

### Model skor (ST)

Tidak ada data pasien untuk melatih XGBoost. Melatih model dengan data karangan juga akan mudah dipatahkan juri. Pendekatan yang dipakai:

- **Skor berbobot gaya Bayes:**
  - Nilai awal tiap penyakit diambil dari prevalensi (SKI 2023 / Profil Kesehatan Kemenkes).
  - Bobot tiap gejala diambil dari literatur, misalnya sensitivitas/spesifisitas atau likelihood ratio.
- **Validasi dengan vignette:** DR menulis kasus contoh lengkap dengan jawaban yang benar. ST mengukur seberapa sering aplikasi menebak dengan benar (top-1, top-3, dan ketepatan rute).
- Angka-angka validasi ini menjadi bahan proposal dan pitch.

### Cara uji coba ke partisipan

Partisipan **tidak memasukkan data kesehatan asli**. Mereka menerima kartu kasus (vignette dari DR), lalu memainkan aplikasi seolah-olah menjadi pasien tersebut. Setelah itu mereka mengisi kuesioner:

- **SUS (System Usability Scale)**
- 3–5 pertanyaan tambahan

Keuntungannya: tidak ada masalah privasi, dan sekaligus mengukur ketepatan triase.

### Poin sehat

- **Bukan** hadiah per jawaban skrining.
- Poin diberikan untuk:
  - menyelesaikan skrining (sekali per keluhan);
  - kembali melapor setelah berobat;
  - cek ulang risiko kronis tiap bulan;
  - menyelesaikan materi edukasi.
- Yang dibangun di prototipe: **lencana/level**.
- Voucher mitra (apotek, laboratorium) cukup masuk pitch sebagai model bisnis.

### Prioritas fitur (MoSCoW)

| Prioritas                                                | Fitur                                                                                                                                                                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must**                                           | Jalur infeksius versi React; halaman awal memilih jalur; usia; VAS; rute merah dengan telepon dan nomor ambulans; hapus label penyakit di pilihan; tombol Mobile JKN; jalur kronis (maks. 4 penyakit); deploy |
| **Should**                                         | Login/registrasi, profil, dan riwayat skrining; skor model ST menggantikan bobot prototipe                                                                                                                    |
| **Could**                                          | Halaman lencana/level dari poin sehat                                                                                                                                                                         |
| **Won't** (cukup disebut di pitch sebagai rencana) | Model ML yang dilatih data nyata, computer vision sungguhan, database faskes dan GPS nyata, penukaran reward                                                                                                  |

---

## 2. Pembagian tugas (kepemilikan)

| Area                                                                                   | Pemilik                                                   | Pendukung                                |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------- |
| Spesifikasi klinis jalur kronis, Blueprint v2, vignette kasus, review semua teks medis | **DR**                                              | ST                                       |
| Model skor, bobot, validasi vignette, desain survei, analisis feedback, visualisasi    | **ST**                                              | DR                                       |
| Database, API triase, simpan skrining, profil, deploy, README                          | **BE**                                              | FE                                       |
| UI React, mesin kuis, semua layar, integrasi API, rekaman demo video                   | **FE**                                              | BE                                       |
| Proposal                                                                               | **DR** (isi klinis) + **ST** (metode & hasil) | BE (arsitektur)                          |
| Pitch deck                                                                             | **ST**                                              | DR, FE (screenshot)                      |
| Video                                                                                  | **FE** (rekam & edit)                               | BE (naskah & narasi), DR (bagian klinis) |
| Rekrut partisipan                                                                      | **Semua**, dikoordinasi **ST**                | —                                       |

---

## 3. Timeline

### Selasa, 13 Okt — fondasi

**Semua — kickoff 30 menit, segera.** Sepakati dokumen ini dan jawab pertanyaan terbuka di bagian 6.

**DR**

1. Pilih maks. 4 penyakit kronis beserta instrumen skrining yang tervalidasi.
2. Isi spesifikasi di [Blueprint-Kronis.md](Blueprint-Kronis.md): pertanyaan, pilihan, red flag, dan aturan rute.
3. Putuskan semua poin "Keputusan DR" di bagian 7.2 dan perbarui [Blueprint.md](Blueprint.md) menjadi v2.
4. Tulis 15 vignette kasus infeksius, masing-masing dengan rute yang benar.

**ST**

1. Kumpulkan data prevalensi dan likelihood ratio gejala dari literatur.
2. Tulis `scoring.py` beserta unit test. Bobot prototipe dipakai sebagai baseline.
3. Buat Google Form survei: persetujuan, SUS, dan pertanyaan tambahan.
4. Sebarkan pendaftaran partisipan (target ≥ 20 orang).

**BE**

1. Bersihkan template: hapus `items`, ganti nama proyek dan README.
2. Pilih hosting dan **deploy versi kosong ("walking skeleton") malam ini**, supaya masalah deploy ketahuan sejak awal.
3. Buat model data `Profile` (tanggal lahir, jenis kelamin, kab/kota) dan `Screening` (jalur, jawaban, hasil, rute, waktu).
4. Pindahkan isi prototipe ke `content/infeksius.json` dan buat endpoint `GET /triage/flows/{flow_id}`.

**FE**

1. Buat token desain dan komponen dasar dari prototipe: kartu ber-tab, tile pilihan, gelembung bicara, maskot, HUD/peta tahap, tombol 3D.
2. Buat mesin kuis yang membaca JSON.
3. Kerjakan semua poin FE di bagian 7.1.

**Batas waktu hari ini**

| Jam   | Target                                                                                           |
| ----- | ------------------------------------------------------------------------------------------------ |
| 21:00 | **Spesifikasi kronis + Blueprint v2 selesai (DR)** — ini syarat utama pekerjaan hari Rabu |
| 21:30 | Sinkronisasi 15 menit                                                                            |

### Rabu, 14 Okt — jalur kronis, deploy, uji coba dimulai

**DR**

1. Jawab pertanyaan FE/BE tentang jalur kronis.
2. Tulis 15 vignette tambahan (infeksius + kronis), total 30.
3. Mulai menulis proposal: latar belakang dan dasar klinis.

**ST**

1. Masukkan bobot jalur kronis.
2. Jalankan validasi pada 30 vignette dan catat hasilnya.
3. Finalkan survei.
4. Atur jadwal partisipan.

**BE**

1. Buat `content/kronis.json` dan endpoint `POST /triage/flows/{flow_id}/score` yang memakai `scoring.py`.
2. Buat endpoint `POST /screenings` dan `GET /screenings/me`.
3. Tambahkan field profil di registrasi.

**FE**

1. Buat UI jalur kronis.
2. Hubungkan semua layar ke API.
3. Buat halaman hasil dengan tombol Mobile JKN.
4. Tata ulang tampilan login/registrasi/profil agar sesuai gaya aplikasi.
5. Buat halaman riwayat (Should).

**Batas waktu hari ini**

| Jam          | Target                                                    |
| ------------ | --------------------------------------------------------- |
| 15:00        | **Deploy v1 (BE + FE)**                             |
| 15:00–17:00 | QA internal oleh keempat anggota, memakai vignette        |
| 17:00        | **Uji coba partisipan dibuka** (sampai Kamis 12:00) |
| 21:30        | Sinkronisasi                                              |

### Kamis, 15 Okt — analisis, perbaikan, persiapan pitch

**ST**

1. 12:00 — tutup survei dan kirim **daftar perbaikan berprioritas** ke FE/BE.
2. 17:00 — selesaikan analisis:
   - skor SUS
   - akurasi vignette
   - tema-tema feedback
   - grafik untuk deck

**DR**

1. Selesaikan draf proposal: latar belakang, solusi, metode klinis.
2. Review semua teks medis di aplikasi.

**FE**

1. Kerjakan perbaikan dari feedback (UI).
2. Rapikan tampilan.
3. Siapkan data demo.

**BE**

1. Kerjakan perbaikan dari feedback (API).
2. Tulis README final: cara menjalankan, arsitektur, screenshot, disclaimer.
3. Buat diagram arsitektur.

**Semua, malam hari — persiapan untuk Jumat**

- **Kerangka pitch deck**, slide demi slide.
- **Naskah dan storyboard video.**
- Isi proposal disesuaikan dengan hasil uji coba.

**Batas waktu hari ini**

| Jam   | Target                                                      |
| ----- | ----------------------------------------------------------- |
| 20:00 | **Feature freeze** — setelah ini hanya perbaikan bug |
| 21:00 | Tag rilis`v1.0` dan deploy final                          |

### Jumat, 16 Okt — luaran

| Jam          | DR                                                            | ST                  | BE                                  | FE                              |
| ------------ | ------------------------------------------------------------- | ------------------- | ----------------------------------- | ------------------------------- |
| 08:00–12:00 | Final proposal                                                | Pitch deck          | Cek deploy, README, kebersihan repo | Rekam demo layar (HP & desktop) |
| 12:00–15:00 | Rekam bagian klinis video                                     | Final deck          | Rekam narasi                        | Edit video                      |
| 15:00–19:00 | Review semua luaran                                           | Review semua luaran | Bantu edit video                    | Final video                     |
| 19:00–21:00 | **Semua: cek ulang checklist di bagian 4, lalu unggah** |                     |                                     |                                 |

---

## 4. Checklist luaran

- [ ] **GitHub**
  - README: deskripsi, fitur, screenshot, arsitektur, cara menjalankan, tim, lisensi, disclaimer.
  - Tidak ada secret asli di repo.
  - Isi bawaan template sudah dibersihkan.
- [ ] **Prototipe**
  - URL yang bisa diakses.
  - Akun demo.
  - Sudah dites di HP Android dan iPhone.
- [ ] **Proposal** — sesuai format panitia.
- [ ] **Pitch deck**
  - masalah → solusi → demo → validasi (SUS + akurasi) → model bisnis/keberlanjutan → tim
- [ ] **Video** — durasi dan format sesuai aturan panitia; sudah ditonton ulang sampai habis.

---

## 5. Risiko dan mitigasi

| Risiko                                                        | Mitigasi                                                                                                                                                     |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Spesifikasi kronis telat, sehingga FE/BE menganggur hari Rabu | Batas waktu Selasa 21:00. Kalau belum siap, FE memakai versi minimal 2 penyakit dulu.                                                                        |
| Deploy bermasalah di hari terakhir                            | Walking skeleton sudah ter-deploy Selasa malam; deploy v1 Rabu 15:00.                                                                                        |
| Partisipan kurang                                             | Rekrut sejak Selasa. Uji coba bisa jarak jauh (link + form). Target minimal 15.                                                                              |
| Juri bertanya "AI-nya di mana?"                               | Jawab jujur: skor Bayes berbasis literatur yang divalidasi vignette, dengan rencana ML setelah ada data. Ini lebih kuat daripada mengaku XGBoost tanpa data. |
| Waktu Jumat habis                                             | Kerangka deck dan naskah video sudah ada sejak Kamis malam; tenggat internal 21:00.                                                                          |

---

## 6. Pertanyaan terbuka (perlu dijawab di kickoff)

1. **"djkn mobile app"** maksudnya aplikasi **Mobile JKN (BPJS Kesehatan)**, kan? (DJKN adalah Direktorat Jenderal Kekayaan Negara, tidak terkait.)
2. Apa **tema dan kriteria penilaian** hackathon? Apakah jalur kronis sesuai tema, mengingat nama proyeknya "tropical disease"?
3. Ketentuan luaran: **durasi video**, template proposal, jumlah slide maksimal?
4. **Hosting**: FastAPI Cloud, VPS (Docker Compose), atau layanan lain? Ada anggaran?
5. **Data diri** apa saja yang dibutuhkan? Usulan: nama, tanggal lahir, jenis kelamin, kab/kota — **tanpa NIK atau nomor BPJS**.
6. **Partisipan uji coba** dari mana (mahasiswa, masyarakat umum, tenaga kesehatan) dan berapa target jumlahnya?
7. Nama masing-masing anggota, dan siapa yang paling longgar waktunya di hari Jumat?

---

## 7. Hasil pengecekan Blueprint.md dan TropiCek-Simulasi.html

Dicek pada 13 Okt 2026 terhadap masukan tim.

- **Blueprint.md** belum memuat satu pun masukan baru.
- **TropiCek-Simulasi.html** masih versi sebelum masukan.

Semua perbaikan dikerjakan di versi React, bukan di file HTML.

### 7.1 Masukan tim yang belum ada

| # | Masukan                                      | Kondisi di Blueprint                        | Kondisi di HTML                                               | Yang dikerjakan                                                                                                                                 | Pemilik       |
| - | -------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| 1 | Pilih jalur infeksius/kronis di halaman awal | Tidak ada                                   | Hanya tombol "Mulai Skrining"                                 | Layar pilih jalur dengan kata-kata pasien: "Saya sedang sakit / ada keluhan baru" dan "Cek risiko penyakit jangka panjang"                      | DR (teks), FE |
| 2 | Usia                                         | Tidak ada                                   | Langkah "Siapa yang sakit?" tanpa usia                        | Usia (tahun; bayi < 1 tahun dalam bulan) dan jenis kelamin di langkah pertama,**sebelum** pertanyaan darurat; terisi otomatis dari profil | DR, FE        |
| 3 | Telepon atau nomor ambulans di rute merah    | —                                          | Hanya tombol`tel:119`                                       | Tambah nomor 119 dan 112 sebagai teks + tombol salin                                                                                            | FE            |
| 4 | Hapus label penyakit di pilihan              | Label "(Suspek …)" adalah catatan internal | Tampil karena "Mode Presentasi" aktif secara default          | Hapus di mode pasien. Nama penyakit hanya di halaman hasil                                                                                      | FE            |
| 5 | VAS                                          | Q9 hanya menyebut "Skala Nyeri"             | Slider angka 0–10 + wajah, posisi awal 5 (bias*anchoring*) | VAS 0–100 tanpa angka dan tanpa posisi awal. Ambang "chikungunya kronis" (di HTML: nyeri ≥ 7) diubah ke skala 0–100                          | FE, ST        |
| 6 | Mobile JKN                                   | Tahap 7 hanya navigasi GPS                  | Tombol Maps + telemedisin (toast simulasi)                    | Tombol "Buat janji dokter (Mobile JKN)"                                                                                                         | FE            |
| 7 | Registrasi, login, data diri                 | Tidak ada                                   | Tidak ada                                                     | Pakai auth bawaan template + field profil; mode tamu tetap default                                                                              | BE, FE        |
| 8 | Poin sehat                                   | Tidak ada                                   | +10 koin per jawaban                                          | Ubah aturan poin sesuai bagian 1                                                                                                                | FE            |

### 7.2 Temuan lain — keputusan DR (paling lambat Selasa 21:00)

1. **Ganti suhu (Q7) untuk klaster B–E.**
   - Blueprint: kalau pasien tidak punya termometer, suhu diganti dengan kurva demam dari Q3.
   - Masalahnya, Q3 hanya berisi pola demam di klaster A (Demam). Di klaster B–E (napas, perut, kulit, bengkak), Q3 tidak membahas demam.
   - HTML tetap menulis "AI memakai kurva demam (Q3)" untuk semua klaster.
   - **Usulan:** untuk klaster B–E, tanya proksi sederhana: "Badan terasa panas/demam?"
2. **Tanda kurung kosong di Blueprint (baris 47, pilihan tifoid).** "...lebih panas di malam hari ( )...". HTML mengisinya dengan "pola anak tangga / stepladder". Mohon dikonfirmasi.
3. **Campak tidak masuk rute mana pun di Tahap 7.** Campak hanya disebut untuk notifikasi ruang isolasi. HTML menaruhnya di rute KUNING. Rute mana yang benar?
4. **"Postur gemuk → prediktor malaria berat" (Q8) perlu sumber.** HTML memakainya: skor malaria +5 dan muncul peringatan di hasil. Kalau tidak ada sumber yang kuat, sebaiknya dihapus.
5. **Peringatan Ibuprofen/Aspirin pada suspek DBD.** Ini tambahan di HTML, tidak ada di Blueprint (Blueprint hanya memuat peringatan Loperamide). Disetujui?
6. **Pilihan cacingan "(Khusus Anak)".** Dengan adanya usia, pilihan ini sebaiknya hanya muncul untuk usia tertentu. Berapa batas usianya? Atau tetap untuk semua umur, karena dewasa juga bisa cacingan?
7. **Klaster E hanya punya satu pilihan.** Memilih "Pembengkakan kronis" praktis sama dengan menjawab filariasis. Perlu pertanyaan pembeda? Misalnya bengkak satu sisi, atau tinggal di daerah endemis.
8. **Rute hijau menyebut "Varicella ringan" tanpa kriteria.** Apa batas ringan vs. berat, dan ke rute mana kalau berat?
9. **Kata "XGBoost".**
   - Tahap 6 menulis XGBoost; layar "berpikir" di HTML menulis "Model XGBoost menghitung…".
   - Teks ini diganti sesuai model ST (skor Bayes) — keputusan ST.

### 7.3 Catatan untuk pitch

- **Kamera AI (Q10) di prototipe adalah simulasi:** pengguna memilih sendiri temuannya. Sebutkan dengan jujur sebagai rencana pengembangan.
- **Navigasi GPS dan "data terkirim ke SATUSEHAT"** juga masih simulasi.
