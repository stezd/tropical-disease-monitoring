# Rencana Kerja TropiCek

**Tenggat:** Jumat, 16 Okt 2026, **23:50 WIB**. Usahakan unggah beberapa jam sebelumnya.

**Yang dikumpulkan:** kode di GitHub · link aplikasi · proposal · slide pitch · video

---

## 1. Siapa mengerjakan apa

| Siapa                     | Tugas utama                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Dokter (DR)**     | Tentukan jalur kronis dan buat kartu kasus (vignette) untuk testing                                                       |
| **Statistika (ST)** | Cara menghitung skor, koordinasi uji coba aplikasi, visualisasi dan olah hasil uji coba. Fitur analisis foto (lihat bawah) |
| **Backend (BE)**    | Server dan database, simpan hasil skrining, akun pengguna, aplikasi online, README                                         |
| **Frontend (FE)**   | Semua tampilan aplikasi, sambungkan ke server                                                                              |

**Fitur foto (jalur infeksi, prioritas rendah):** pengguna diminta mengunggah foto (misalnya ruam atau bengkak) untuk membantu skrining. ST yang mengembangkan, **target selesai Rabu**. Bebannya bisa besar, jadi kerjakan setelah rumus skor beres. Kalau Rabu belum jadi, pakai tampilan simulasi (pengguna memilih temuan sendiri) dan sebut sebagai rencana pengembangan.

**Luaran akhir:**

- **Proposal:** DR (isi medis) + data dibantu yang lain
- **Slide pitch:** ST + data dibantu yang lain
- **Cari peserta uji coba:** semua, dikoordinasi ST

---

## 2. Urutan kerja (kira-kira)

**Selasa — siapkan dasar**

- DR: tentukan penyakit dan alur jalur kronis, lalu mulai tulis kartu kasus untuk testing.
- ST: mulai rumus skor, buat Google Form survei, mulai cari peserta. Setelah rumus skor jalan, mulai fitur foto.
- BE: bersihkan kode dan deploy ASAP
- FE: mulai pindahkan tampilan simulasi HTML ke aplikasi asli.

**Rabu — jalur kronis, aplikasi online, uji coba mulai**

- Jalur kronis dibuat.
- Fitur foto selesai (opsional)
- Deploy Aplikasi dan dicoba tim sendiri dulu.
- Setelah itu, bagikan survei.

**Kamis — olah hasil, perbaiki**

- ST olah hasil survei, masukan ke pitchdeck
- FE/BE revisi app sesuai perbaikan
- DR selesaikan draf proposal.
- Malam: berhenti menambah fitur. Mulai susun slide dan naskah video.

**Jumat — luaran**

- Selesaikan proposal, slide, dan video.

---

## 3. implementasi tambahan

Simulasi HTML hanya contoh tampilan. Perubahan ini dibuat di aplikasi asli:

1. **Halaman awal:** pilih "Saya sedang sakit" atau "Cek risiko penyakit jangka panjang".
2. **Usia dan jenis kelamin** ditanya paling awal.
3. **Kondisi gawat:** tampilkan tombol telepon 119 dan nomor 119/112 yang bisa disalin. Tanpa koin atau animasi.
4. **Nama penyakit tidak muncul di pilihan jawaban,** hanya di halaman hasil.
5. **Skala nyeri** berupa garis polos tanpa angka, dari "Tidak nyeri" sampai "Nyeri terburuk". Penanda belum ada sebelum disentuh.
6. **Tombol "Buat janji dokter (Mobile JKN)"** di halaman hasil.
7. **Login opsional.** Orang tetap bisa skrining tanpa akun.
8. **Koin tidak diberikan per jawaban.** Koin untuk menyelesaikan skrining, kontrol setelah berobat, atau cek rutin.

---

## 4. Pertanyaan untuk Dokter

1. **Suhu tubuh:** kalau pasien tidak punya termometer di keluhan selain demam (napas, perut, kulit, bengkak), cukup tanya "Badan terasa panas?"?
2. **Tifoid:** di Blueprint ada kurung kosong "( )". Apakah isinya "pola demam naik bertahap"?
3. **Campak** masuk rute mana?
4. **"Badan gemuk → malaria berat":** ada sumbernya? Kalau tidak, dihapus.
5. **Peringatan jangan minum Ibuprofen/Aspirin** untuk dugaan DBD: setuju ditambahkan?
6. **Cacingan:** pilihan ini hanya untuk anak (batas usia berapa) atau semua umur?
7. **Bengkak menahun:** perlu pertanyaan tambahan supaya tidak langsung dianggap filariasis?
8. **Cacar air ringan vs. berat:** apa bedanya, dan yang berat dirujuk ke mana?
9. apakah ada vignette
10. **Tulisan "XGBoost"** di Blueprint diganti sesuai cara hitung ST.

---

# 5. Ingat

- **Jujur soal "AI".** Skor dihitung dari data literatur dan diuji dengan kartu kasus dokter. Fitur foto (kalau belum selesai), GPS, dan kirim data ke SATUSEHAT masih simulasi, jadi sebut sebagai rencana.
- **Uji coba pakai kartu kasus,** bukan data kesehatan asli peserta. Peserta mengisi survei kemudahan pakai (SUS).
- **Jangan pakai kata "diagnosis"** di aplikasi. Pakai "skrining" atau "perkiraan".
- **Jangan minta NIK atau nomor BPJS.**
