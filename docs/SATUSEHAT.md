# Integrasi SATUSEHAT — TropiCare

Status per Oktober 2026: **Tier 1 (Master Sarana Index / MSI) disepakati & tervalidasi via probe; tahap implementasi endpoint & mirror.** Tier 2 (push FHIR Patient/Encounter/Condition) sengaja tidak dilakukan demi prinsip privasi dan batas etika skrining medis.

---

## 1. Landasan Keputusan Arsitektur

TropiCare memosisikan SATUSEHAT sebagai **penyedia data fasilitas pelayanan kesehatan (faskes rujukan)**, bukan penyimpan rekam medis pasien. Dua pertimbangan utamanya:

1. **Privasi Data & Prinsip Anonimitas (UU No. 27/2022 PDP):**
   - TropiCare dirancang dapat digunakan tanpa login dan tanpa identitas pribadi (tidak menanyakan NIK, nama lengkap, tanggal lahir presisi, atau nomor BPJS).
   - Pengiriman resource FHIR (`Encounter`, `Condition`, `Observation`) mewajibkan kaitan ke resource `Patient` resmi yang terverifikasi Dukcapil via NIK. Meminta NIK pasien demi integrasi API akan merusak sifat anonim aplikasi dan melanggar prinsip *data minimization*.

2. **Batas Kewenangan Skrining vs Diagnosis Medis:**
   - TropiCare adalah alat skrining mandiri awal, bukan penegak diagnosis definitif.
   - Mengunggah diagnosis (`Condition` ICD-10) langsung ke rekam medis nasional tanpa pemeriksaan dokter secara tatap muka berisiko menimbulkan *medical error* dan masalah pertanggungjawaban hukum faskes.
   - **Solusi yang diterapkan:** Hasil skrining dikemas menjadi **QR Rangkuman Pasien** (kode ringkas berisi perkiraan, daftar keluhan, dan saran lab). Pasien membawa QR ini ke Puskesmas/RS; dokter faskes memindai dan memutuskan pencatatan ke RME resmi masing-masing.

---

## 2. Ruang Lingkup: Tier 1 (Master Sarana Index / MSI Mirror)

Menggantikan tautan pencarian teks umum di Google Maps dengan **nama faskes terverifikasi, kode resmi SATUSEHAT, dan koordinat presisi**.

### Hasil Validasi (Oktober 2026)
Pengujian langsung terhadap Sandbox SATUSEHAT (`https://api-satusehat-stg.dto.kemkes.go.id`), dilanjutkan sinkronisasi nasional penuh ke database lokal.

- **Autentikasi:** Endpoint `/oauth2/v1/accesstoken` via `client_credentials`.
  - Respon mengembalikan `expires_in` sebesar `14399` (~4 jam, berbeda dari contoh dokumentasi `3599`). Cache token wajib membaca nilai TTL dinamis ini.
- **Batas Ukuran Halaman:** Dokumentasi MSI menyebut `limit` maksimum `2000`, tetapi gateway Apigee mengembalikan `502 TooBigBody` di atas ~1500. Sinkronisasi memakai `limit=1000` untuk margin aman.
- **Kualitas Koordinat** — diukur dari 67.070 baris (sinkronisasi penuh 102+104+105, dijalankan sekali khusus untuk pengukuran ini):

  | Jenis             | Total   | Punya koordinat | Persentase |
  | ----------------- | ------- | --------------- | ---------- |
  | `102` Puskesmas   | 10.376  | 10.373          | **100%**   |
  | `104` Rumah Sakit | 3.571   | 3.427           | **96%**    |
  | `105` Apotek      | 53.123  | 1.138           | **2,1%**   |

  - **Penting:** angka "92%" dari probe awal adalah artefak sampling. Probe hanya mengambil 3 halaman pertama MSI, yang didominasi Posyandu (4.875 dari 6.000 baris) — jenis yang tidak dipakai TropiCare. Tabel di atas adalah pengukuran sebenarnya.
  - Konsekuensi: pengurutan jarak (*haversine*) **layak** untuk Puskesmas dan RS (rute KUNING dan MERAH), tetapi **tidak layak** untuk Apotek (rute HIJAU). Karena itu apotek dikecualikan dari sinkronisasi default.
  - Setelah filter status/operasional, mirror berisi **13.930 faskes** (10.374 Puskesmas + 3.556 RS) dengan **99% berkoordinat**. Waktu sinkronisasi turun dari ~78 halaman menjadi **15 halaman (~20 detik)**.
- **Kategori Sarana (Jenis Sarana):**
  - `102` Puskesmas: ~10.376 unit, 100% berkoordinat.
  - `104` Rumah Sakit (rujukan IGD / kondisi gawat): ~3.571 unit, 96% berkoordinat.
  - `105` Apotek: ~53.123 unit, hanya 2,1% berkoordinat. **Tidak disinkronkan secara default**; aktifkan dengan `--include-apotek`.
  - Sinkronisasi default (102+104): ~14.000 baris, ~14 halaman pada `limit=1000`.
  - Pengambilan data mendukung filter multi-jenis dalam satu panggilan (parameter `jenis_sarana` berulang).
- **Status Operasional:**
  - Filter sinkronisasi menyertakan `verified` dan `valid`, serta mengecualikan `draft`/`review`.
  - Faskes non-operasional (`operasional=false`) difilter keluar.
- **Kualitas Data Lain:**
  - 17 baris MSI tidak memiliki provinsi (`provinsi.kode` dan `nama` kosong). Baris seperti ini tidak mungkin dikembalikan endpoint (yang mensyaratkan `province`), jadi dibuang saat sinkronisasi.
  - `alamat` kosong pada ~35% baris dan `telp` pada ~89% baris — jangan diasumsikan selalu ada.
- **Penyelarasan Nama Wilayah:**
  - Dari 38 provinsi di `frontend/src/features/triage/location.ts`, 37 provinsi identik dengan data MSI.
  - Terdapat 1 perbedaan: MSI mencatat kode 34 sebagai `"Yogyakarta"`, sementara front-end menggunakan `"Daerah Istimewa Yogyakarta"`. Adapter menerima nama, alias, maupun kode (`"34"`).

---

## 3. Pola Integrasi: Local Mirror (Bukan Runtime Proxy)

```
[Kemenkes SATUSEHAT MSI]
        │
        │ Batch sync (CLI / cron)
        ▼
[PostgreSQL TropiCare: tabel 'facility']
        ▲
        │ GET /api/v1/facilities?province=...&kind=...
        ▼
[Browser Pasien (React)]
        │
        ├─ Hitung jarak terdekat (haversine) di perangkat pasien
        ├─ Koordinat GPS TIDAK PERNAH dikirim ke server TropiCare
        └─ Buka navigasi peta langsung ke nama faskes spesifik
```

**Keuntungan Pola Mirror:**
1. **Ketahanan Rute Gawat Darurat (MERAH):** Pasien dalam kondisi gawat darurat tetap mendapatkan navigasi faskes terdekat tanpa hambatan meski server Kemenkes sedang gangguan (*down* / *maintenance*).
2. **Nol Latensi Eksternal:** Permintaan faskes dilayani langsung dari database internal.
3. **Privasi Koordinat:** Koordinat pengguna hanya diproses di browser lokal untuk memilih faskes terdekat dari daftar faskes dalam satu provinsi. Server tidak pernah menerima titik lintang/bujur pengguna.
4. **Fallback Halus:** Jika sinkronisasi belum dijalankan atau database kosong, tombol rujukan kembali ke pencarian Google Maps umum seperti sebelumnya.

---

## 4. Konfigurasi Lingkungan

Variabel lingkungan yang digunakan:
```env
# SATUSEHAT Sandbox / Production
SATUSEHAT_ENV=sandbox
SATUSEHAT_CLIENT_ID=<client_id_dari_portal>
SATUSEHAT_CLIENT_SECRET=<client_secret_dari_portal>
SATUSEHAT_ORG_ID=<organization_id>
```

Skrip probe diagnostik:
```bash
cd backend
uv run --env-file ../.env python scripts/satusehat_probe.py --check-provinces
```
