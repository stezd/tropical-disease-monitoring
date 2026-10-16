# 5 Rencana Monetisasi Paling Realistis

Semua angka adalah asumsi yang belum divalidasi. Uji dulu lewat survei harga dan wawancara calon klien.

**Aturan untuk semua rencana:**
- Skrining inti dan peringatan bahaya tetap gratis.
- Tidak ada tawaran beli di layar MERAH atau saat hasil keluar.
- Data skrining per individu tidak dijual.
- Sumber data dasbor dan surveilans (ide 1 di bawah dan surveilans Dinkes): tabel `screening_stat`, satu baris tanpa identitas langsung per skrining selesai (tamu juga).
- Aturan k = 10: kelompok kurang dari 10 orang disembunyikan di setiap agregat.
- Data ini "tanpa identitas langsung", **bukan "anonim"**: kombinasi usia, jenis kelamin, provinsi, dan gejala secara teori masih bisa mengidentifikasi. UU PDP tetap berlaku (data kesehatan = data pribadi spesifik).
- Sebelum dipakai pasien sungguhan, teks privasi perlu ditinjau DR dan sebaiknya ahli hukum.

---

## 1. Dasbor Klinik/Puskesmas

**Masalah**
- Petugas mengulang wawancara untuk setiap pasien.
- Tidak ada pra-triase, jadi pasien gawat dan ringan antre sama.
- Klinik tidak punya rekap keluhan.

**Solusi**
- Pasien menunjukkan QR rangkuman, petugas memindai.
- Pasien masuk antrean, diurutkan MERAH → KUNING → HIJAU.
- Rekap harian/bulanan dan ekspor CSV.
- Beberapa akun staf.

**Pricing**
- Dasar: Rp250 rb/bulan (≤ 3 staf).
- Standar: Rp400 rb/bulan atau Rp4 jt/tahun (≤ 10 staf, ekspor, rekap).
- Pilot gratis 3 bulan, lalu tagih lewat invoice.

---

## 2. Skrining Karyawan

**Masalah**
- Perusahaan di daerah endemis malaria (tambang, perkebunan) butuh skrining berkala tapi tidak punya alat.
- HR tidak boleh melihat data kesehatan individu.

**Solusi**
- Kode kampanye per perusahaan.
- Karyawan skrining dan melihat hasil sendiri.
- HR hanya melihat agregat: partisipasi dan sebaran rute (sel < 10 orang disembunyikan).
- Kontrak melarang pemakaian hasil untuk keputusan kerja.

**Pricing**
- Rp30 rb/karyawan/tahun, minimal 200 karyawan.
- Setup Rp5 jt, sekali bayar (rincian di bawah).
- Contoh tahun pertama, 300 karyawan: Rp5 jt + Rp9 jt = **Rp14 jt**.

**Isi setup (Rp5 jt)**
- Buat organisasi + kampanye: kode, periode, batas minimal sel agregat.
- Akun admin HR + panduan membaca dasbor agregat.
- Materi sosialisasi: poster/pesan WhatsApp, penjelasan privasi (HR tidak melihat hasil individu).
- Briefing HR dan petugas K3, 1–2 jam (daring).
- Uji coba dengan beberapa karyawan sebelum peluncuran.
- Laporan pertama: partisipasi dan sebaran rute.
- **Tidak termasuk:** pemeriksaan medis, dokter di lokasi, pelatihan tatap muka di luar kota.

---

## 3. TropiCare Plus (pemantau PTM)

**Masalah**
- Penderita hipertensi atau diabetes perlu memantau tensi dan gula terus-menerus.
- Catatan kertas hilang, dan dokter tidak punya riwayat.

**Solusi**
- Riwayat tanpa batas dan grafik tren tensi, GDS, berat, lingkar perut.
- Pengingat cek ulang dan ekspor PDF untuk dokter.
- Versi gratis: catat angka dan riwayat 30 hari.
- Peringatan bahaya tetap gratis.

**Pricing**
- Rp15 rb/30 hari atau Rp150 rb/tahun (setara 10 bulan).
- Coba gratis 14 hari.
- Keluarga (≤ 5 profil): Rp25 rb/30 hari.
- Prabayar (QRIS/e-wallet), bukan auto-debit.

---

## 4. White-label

**Masalah**
- LSM kesehatan dan program donor butuh aplikasi skrining, tapi tidak punya tim teknis dan dokter untuk bank soal.

**Solusi**
- Mesin dan bank soal TropiCare dengan nama, logo, dan warna klien.
- Satu deployment per klien, kustom konten lewat konfigurasi (mis. hanya malaria).
- Kontrak: perubahan medis wajib OK DR.
- Yang dijual jasa dan dukungan, bukan kode (kode MIT).

**Pricing**
- Setup Rp30 jt (sekali bayar) + Rp3 jt/bulan.
- Rp3 jt/bulan menutup hosting, pembaruan, dan dukungan.
- Kustom konten (pertanyaan atau bobot baru) ditagih terpisah, butuh OK DR dan ST.
- Contoh tahun pertama: Rp30 jt + Rp36 jt = **Rp66 jt**.

**Isi setup (Rp30 jt)**
- Tema merek: nama, logo, maskot, warna.
- Deployment Railway terpisah, domain klien, SSL.
- Konfigurasi konten: pilih penyakit atau alur yang aktif (mis. hanya malaria).
- Teks hukum atas nama klien: kebijakan privasi dan persetujuan.
- Kontrak + DPA (klien = pengendali data) + klausul "perubahan medis wajib OK DR".
- Uji alur, rute MERAH, dan QR; pelatihan admin klien.
- Dokumentasi pengelolaan.

**Catatan setup**
- Bisa dicicil: 50% di awal, 50% saat serah terima. Atau dimasukkan ke proposal hibah klien.
- Setup bukan pendapatan berulang. Jangan dihitung lagi di tahun berikutnya.
- Setup klien pertama lebih berat (sistem tema belum ada). Beri harga lebih rendah dengan imbalan testimoni.
- Hitung jam kerja sebenarnya setelah klien pertama, lalu sesuaikan harga.

---

## 5. Donasi

**Masalah**
- Biaya server dan AI harus ditutup, dan pengguna ingin mendukung tanpa langganan.

**Solusi**
- Halaman "Dukung" dengan QRIS statis atau Saweria/Trakteer.
- Laporan penggunaan dana berkala.
- Tidak ada fitur yang dikunci untuk donatur.

**Pricing**
- Pilihan Rp10 rb / 25 rb / 50 rb / bebas.
- Tanpa payment gateway.

---

## Proyeksi Tahun ke-3 (moderat)

| Rencana | Asumsi | Pendapatan |
| --- | --- | --- |
| Dasbor Klinik | 30 lokasi × Rp400 rb × 12 | Rp144 jt |
| Plus | 500 pelanggan × Rp15 rb × 12 | Rp90 jt |
| White-label | 1 klien lama + 1 baru | Rp84 jt |
| Skrining Karyawan | 4 perusahaan (2 baru) | Rp70 jt |
| Donasi | — | Rp6 jt |
| **Total** | | **≈ Rp394 jt** |

- Biaya Th3 ≈ Rp76 jt (server, AI, legal, penjualan, honor DR, pajak). Laba ≈ Rp318 jt, **belum termasuk gaji tim**.
- Titik impas biaya server: ±8 pelanggan Plus, atau 1 klinik selama 4 bulan.
- Konservatif Th3 sekitar Rp53 jt laba. Optimis sekitar Rp1,2 M.

## Urutan

1. **Validasi:** survei harga + wawancara 5 klinik.
2. **Donasi + badan hukum.**
3. **Pilot** Dasbor Klinik dan Skrining Karyawan (tagih manual).
4. **Plus**, setelah payment gateway ada.
5. **White-label**, bila ada klien.

## Perlu diputuskan

- **Tim:** monetisasi atau tidak, bentuk badan hukum.
- **DR:** teks Plus (label, peringatan), klausul medis white-label.
- **ST:** survei harga dan asumsi proyeksi.
