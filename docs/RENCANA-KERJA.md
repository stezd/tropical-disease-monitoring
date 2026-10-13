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
