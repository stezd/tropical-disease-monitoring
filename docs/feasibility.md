# Feasibility TropiCare

## 1. Biaya rutin

| Komponen | Sekarang | Biaya | Catatan |
| --- | --- | --- | --- |
| Railway (web + PostgreSQL) | Hobby plan | Rp90 rb/bulan | Pasang `railway usage limit` |
| AI (OpenRouter) | Kredit berbayar $10 (sekali beli) | ≈ Rp160 rb, habis-pakai | Batas harian model gratis naik jadi 1000 (`TRIAGE_AI_RPD_LIMIT=1000`) |
| Domain | Mungkin domain Railway | ≈ Rp15 rb–250 rb/tahun | Beli domain sendiri supaya link QR stabil |

**Total tetap: ≈ Rp90 rb/bulan + domain (tahunan).** AI bersifat habis-pakai, bukan bulanan.

### Estimasi domain

Harga berubah per registrar, cek sebelum beli. Tahun pertama sering lebih murah dari perpanjangan.

| Domain | Perkiraan/tahun | Syarat |
| --- | --- | --- |
| `.my.id` / `.web.id` | Rp15 rb–100 rb | Perorangan, KTP |
| `.id` | Rp200 rb–350 rb | Perorangan atau lembaga |
| `.or.id` | Rp50 rb–150 rb | Dokumen organisasi/yayasan |
| `.co.id` | Rp300 rb–400 rb | Dokumen badan usaha |
| `.com` / `.org` | Rp150 rb–250 rb | Tanpa syarat |

- Saran: `.id` atau `.org` untuk kesan resmi. `.my.id` cukup untuk uji coba.
- Domain kustom di Railway tanpa biaya tambahan dan SSL otomatis (perlu dicek di plan Anda).
- Daftarkan atas nama organisasi, bukan pribadi, bila sudah ada badan hukum.

### Menjaga biaya AI

- Fallback berbayar kira-kira Rp20–30 per pasien (perkiraan README). Kalau semua pasien memakainya, $10 cukup untuk ≈ 5.000–8.000 skrining.
- Pakai `TRIAGE_AI_MODEL=...:free` sebagai utama dan model berbayar hanya sebagai fallback, supaya kredit awet.
- Kurs Rp16.000/$ adalah asumsi. Sesuaikan.
- Hitung biaya per skrining sebenarnya dari log AI dan `railway metrics`.
- Aktifkan batas pengeluaran per kunci di OpenRouter. Matikan auto top-up.
- Kartu pembayaran Railway dan OpenRouter atas nama satu orang. Catat pemiliknya di daftar akun (bagian 3).

## 2. Sumber dana

| Opsi | Catatan |
| --- | --- |
| Hibah / inkubator / lomba lanjutan | Biaya server kecil, jadi permintaan dana realistis |
| Kerja sama Dinkes / Puskesmas | Juga membuka jalan ke SATUSEHAT production |
| CSR / sponsor | Hindari sponsor yang berkepentingan dengan hasil (mis. produsen obat) |
| **Dilarang** | Menjual atau membagikan data skrining |

## 3. Administrasi

**Akun** (minimal 2 admin per akun, kredensial di password manager bersama):
GitHub · Railway · OpenRouter · domain · email `FIRST_SUPERUSER`

| Hal | Yang perlu dilakukan | Kapan |
| --- | --- | --- |
| Badan hukum | Yayasan, CV, atau di bawah kampus. Perlu untuk kontrak, hibah, dan daftar PSE Lingkup Privat (Komdigi) | Sebelum dipakai publik |
| SATUSEHAT production | Butuh fasyankes berizin. Tanpa mitra, tetap di sandbox | Bila ada mitra |
| Kemenkes | Tanyakan: apakah ini alat kesehatan yang butuh izin edar? | Sebelum peluncuran |
| UU PDP (27/2022) | Kebijakan privasi, masa simpan riwayat, penanggung jawab data, prosedur kebocoran (3×24 jam) | Sebelum pasien sungguhan |
| Isi medis | DR setujui teks, ST setujui bobot, catat nama + tanggal di Acuan-Medis. Tanpa dokter: bekukan isi + tampilkan tanggal tinjauan | Berkelanjutan |
| Lisensi | `LICENSE` masih atas nama pembuat template. Putuskan pemegang hak cipta dan lisensi isi medis | Segera |

## 4. Operasional minimal

- Sync faskes lewat cron Railway.
- Healthcheck + restart `ON_FAILURE` + monitor uptime gratis.
- Ganti secret berkala, dan setiap ada anggota keluar.
- Tanda bahaya dicek di browser, jadi layar MERAH + 119 tetap jalan saat server mati.

## 5. Ide monetisasi

**Batasan:**
- Skrining inti **tetap gratis**: kuesioner, rute, MERAH + 119, QR, faskes, penafian.
- Payment gateway butuh akun merchant + KYC, jadi butuh badan hukum.
- Jangan jual produk berdasarkan hasil skrining.

### 5.1 B2C (perorangan)

| Ide | Yang dibayar | Risiko |
| --- | --- | --- |
| 1. Pemantau PTM (langganan) | Grafik tensi, GDS, berat, lingkar perut + pengingat + ekspor PDF | Data lebih banyak (UU PDP). Ambang butuh DR (K22, K32) |
| 2. Paket Keluarga (langganan) | Banyak profil (anak, lansia), riwayat per anggota | Data anak butuh persetujuan orang tua |
| 3. Pengingat obat | Alarm obat resep dokter (TBC, hipertensi) | Hanya mengingatkan, tidak merekomendasikan obat |
| 4. Kosmetik Kak Tropi (sekali beli) | Kostum, tema, stiker | Tidak muncul saat sakit/MERAH. Tanpa loot box |
| 5. Donasi QRIS | Seikhlasnya | Kecil dan tidak pasti |

- Konversi B2C kemungkinan rendah (pengguna berpenghasilan rendah, pakai BPJS).
- Ide 1 dan 2 paling kuat. Harga masih asumsi.

### 5.2 B2B / B2G (institusi)

| Ide | Pembeli | Isi |
| --- | --- | --- |
| 6. Dasbor Puskesmas/Klinik | Puskesmas, klinik | Scan QR → antrean pra-triase + statistik. Dasbor terpisah, bukan integrasi |
| 7. Surveilans wilayah | Dinkes | Tren keluhan per provinsi. Agregat dari data tanpa identitas langsung, ada batas minimal per sel |
| 8. Skrining karyawan | Tambang/perkebunan endemis | Perusahaan hanya lihat agregat, tidak hasil individu |
| 9. Paket UKS | Sekolah, yayasan | Skrining cacingan, kulit, demam + edukasi |
| 10. White-label | LSM, program donor | Mesin + bank soal dengan merek mereka |

- Semua butuh kontrak. Ide 7 dan 8 butuh klausul baru di teks consent.
- Sumber data ide 6 sampai 8 (dasbor, surveilans): tabel `screening_stat`, satu baris tanpa identitas langsung per skrining selesai. Aturan k = 10: kelompok kurang dari 10 orang disembunyikan.
- Data itu "tanpa identitas langsung", bukan "anonim"; UU PDP tetap berlaku. Teks privasi perlu ditinjau DR dan sebaiknya ahli hukum sebelum dipakai pasien sungguhan.
- Asuransi tidak dimasukkan: data skrining tidak boleh menentukan premi atau klaim.

### 5.3 Urutan saran

1. **Validasi dulu.** Tambah 1–2 pertanyaan kesediaan membayar di survei SUS. Tanpa kode.
2. **Termurah:** donasi QRIS statis (gambar QR, tanpa API).
3. **Serius:** dahulukan B2G/B2B (ide 6 atau 7). Satu kontrak Dinkes bisa menutup ongkos server bertahun-tahun.
