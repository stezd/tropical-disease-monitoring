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

## Opsi tambahan: API untuk Mitra

Belum masuk 5 rencana utama: volume awal kecil dan risikonya lebih banyak. Versi ringan dari White-label.

**Masalah**
- Aplikasi mitra (telemedisin, vendor rekam medis klinik, aplikasi kesehatan karyawan, LSM) butuh skrining tapi tidak punya bank soal dan aturan rute yang disetujui dokter.
- Membangun sendiri mahal dan butuh DR dan ST.

**Solusi: 3 produk API**
- **Skoring** (`POST /flows/{id}/score`): jawaban masuk, perkiraan + rute + peringatan keluar. Endpoint ini sudah stateless ("nothing is saved").
- **Konten**: bank soal dan opsi (`GET /flows/{id}`) tanpa bobot, supaya mitra memakai kuesioner yang sama.
- **Statistik agregat**: tren per wilayah untuk Dinkes dan peneliti (dari `screening_stat`). Hanya agregat, kelompok < 10 disembunyikan.
- **Tidak dijual:** baris per orang (`screening_stat` mentah), data faskes turunan SATUSEHAT (syarat lisensi belum jelas).

**Pagar privasi (wajib)**
- TropiCare = pemroses data, mitra = pengendali data. Perlu DPA. Persetujuan pengguna ada di sisi mitra.
- Skema API menolak nama, NIK, nomor telepon, dan koordinat. Kolom teks bebas obat dimatikan di jalur API.
- Mode **aturan saja** (tanpa model AI luar): data tidak keluar dari server TropiCare. Mode AI hanya bila mitra setuju data ke OpenRouter/Google.
- Isi permintaan tidak disimpan dan tidak masuk log. Hanya hitungan per klien per hari.
- Statistik: kelompok < 10 disembunyikan, rentang tanggal dibatasi ke minggu penuh, kuota kueri per klien, supaya selisih dua kueri tidak membuka kelompok kecil.
- Kontrak: dilarang mencocokkan keluaran API dengan identitas untuk keputusan kerja, asuransi, atau kredit.
- Penafian "skrining, bukan diagnosis" wajib tampil di aplikasi mitra.

**Yang dibangun**
- Tabel klien API (kunci disimpan sebagai hash), kuota per paket, penghitung pemakaian tanpa isi permintaan.
- Dependency kunci API + batas laju per klien, awalan `/partner/v1`, versi API.
- Sandbox (kunci uji, mode aturan) dan dokumentasi dari OpenAPI.
- Penagihan manual (invoice) dulu. Gateway pembayaran menyusul.

**Pricing (asumsi)**
- Sandbox gratis: 1.000 panggilan/bulan, mode aturan.
- Biaya platform Rp1–2 jt/bulan per mitra.
- Per panggilan: aturan Rp50–100, AI Rp300 (biaya AI ≈ Rp20–30 per skrining, jadi margin ≥ 10×).
- Statistik agregat: lisensi tahunan, Rp15–40 jt per wilayah (digabung dengan ide Surveilans).
- Contoh: 5 mitra × (Rp1,5 jt + 20.000 panggilan × Rp100) ≈ Rp3,5 jt/bulan ≈ **Rp42 jt/tahun**. Tidak dihitung di proyeksi utama.

**Risiko**
- **Tanggung jawab medis:** keluaran dipakai di produk pihak lain. Perlu penafian, batas penggunaan di kontrak, dan OK DR. Bisa memperbesar pertanyaan izin alat kesehatan (tanya Kemenkes dulu).
- **Rantai persetujuan:** bila mitra tidak meminta persetujuan pengguna, risiko hukum ikut ke kita.
- **Lisensi:** kode MIT, jadi mitra boleh menjalankan sendiri. Yang dijual layanan dan bank soal. Lisensi isi medis perlu diputuskan (lihat feasibility.md bagian 3).
- **Biaya AI melonjak:** pasang kuota dan harga per panggilan, jangan paket tak terbatas.
- **Beban dukungan:** batasi jumlah mitra awal.

**Penilaian:** layak setelah ada 1–2 mitra yang nyata. Mulai dengan Skoring mode aturan, karena privasinya paling kuat dan biayanya paling kecil. Statistik agregat menyusul bersama ide Surveilans, setelah aturan selisih kueri diuji.

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
6. **API untuk Mitra**, setelah ada 1–2 mitra nyata (mulai dari Skoring mode aturan).

## Perlu diputuskan

- **Tim:** monetisasi atau tidak, bentuk badan hukum.
- **DR:** teks Plus (label, peringatan), klausul medis white-label dan API (batas penggunaan, penafian).
- **ST:** survei harga dan asumsi proyeksi.
