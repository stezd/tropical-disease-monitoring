# Integrasi SATUSEHAT — TropiCare

> **Status 16 Okt 2026: tim memutuskan tidak mengintegrasikan SATUSEHAT lebih lanjut.** Dokumen ini hanya mencatat apa yang sudah dibangun. Kode mirror faskes (`backend/scripts/sync_facilities.py`, tabel `facility`, `/facilities`) masih ada dan dipakai fitur "faskes terdekat"; itu perlu diputuskan: dipertahankan (butuh kredensial SATUSEHAT untuk sinkronisasi) atau diganti sumber lain. Jangan membangun fitur baru di atasnya sebelum diputuskan.

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

Menggantikan tautan pencarian teks umum di Google Maps dengan **nama faskes terverifikasi, kode resmi SATUSEHAT, dan koordinat**. Koordinat MSI tidak presisi (lihat §5 nomor 9) — koordinat dipakai untuk *mengurutkan* jarak, sedangkan tautan navigasi mencari **nama** faskes.

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
  - **Catatan penting:** "punya koordinat" ≠ "koordinat benar". Satu Puskesmas contoh meleset **3 km**, dan sebagian baris bahkan berkoordinat di luar provinsinya sendiri (§5 nomor 9). Jadi urutan terdekat bersifat **perkiraan**, dan tautan navigasi sengaja memakai nama faskes, bukan titik koordinat.
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
        ├─ Hitung jarak terdekat (haversine) di perangkat pasien   ← jalur default
        ├─ POST /api/v1/facilities/nearest (koordinat kirim)         ← opt-in
        └─ Buka navigasi peta langsung ke nama faskes spesifik
```

**Dua jalur pemilihan faskes terdekat:**

1. **Default (privasi terjaga):** browser mengambil daftar faskes satu provinsi
   (`GET /facilities`), lalu mengurutkan sendiri berdasarkan jarak. Hanya nama
   provinsi yang sampai ke server; koordinat pengguna tetap di perangkat.
2. **Opt-in (akurasi lintas provinsi):** `POST /api/v1/facilities/nearest`
   menerima koordinat dan mengembalikan faskes terdekat terurut. Hanya aktif
   bila `VITE_FACILITIES_SERVER_NEAREST=true`. Koordinat dikirim di **body**
   (bukan URL) agar tidak tercatat di access log, dipakai sekali untuk menghitung
   jawaban, dan **tidak disimpan**.

Urutan terdekat memakai jarak sebagai sinyal utama; dua faskes yang berjarak
hampir sama (selisih < 0,5 km) diurutkan berdasarkan kelengkapan data (ada
telepon → ada alamat → status `verified`/`valid`). **Faskes yang punya nomor
WhatsApp selalu di atas** — merekalah yang bisa dihubungi pasien dari rumah.
Daftar menampilkan **5** faskes (`NEARBY_LIMIT`); jalur opt-in meminta 20 baris
(`FETCH_POOL`) sebelum mengurutkan ulang, supaya faskes ber-WhatsApp yang agak
jauh tetap bisa naik. Tombol **Rute mencari nama faskes**, bukan koordinat (§5
nomor 9).

**Keuntungan Pola Mirror:**
1. **Tidak ada ketergantungan saat permintaan.** Layar hasil tidak pernah menunggu Kemenkes. (Catatan: rute MERAH tidak memakai mirror sama sekali — layar darurat memakai tautan pencarian Google Maps dan nomor 119, jadi ia tetap hidup apa pun yang terjadi pada mirror.)
2. **Nol Latensi Eksternal:** Permintaan faskes dilayani langsung dari database internal.
3. **Privasi Koordinat:** Pada jalur default, koordinat pengguna hanya diproses di browser lokal untuk memilih faskes terdekat dari daftar faskes dalam satu provinsi; server tidak menerima titik lintang/bujur pengguna. Endpoint opt-in `POST /facilities/nearest` adalah satu-satunya pengecualian: koordinat sampai ke server kita sendiri, dihitung sekali, tidak disimpan, dan tidak pernah diteruskan ke pihak ketiga.
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

Front-end (dibaca saat build; di Railway jadi *build arg*, lihat `backend/Dockerfile`):
```env
# "true" = server yang mengurutkan faskes terdekat (koordinat dikirim).
# Kosong = browser yang mengurutkan (koordinat tetap di perangkat).
VITE_FACILITIES_SERVER_NEAREST=true
```

Skrip probe diagnostik:
```bash
cd backend
uv run --env-file ../.env python scripts/satusehat_probe.py --check-provinces
```

Sinkronisasi mirror faskes ke database lokal:
```bash
cd backend
# Default: Puskesmas (102) + Rumah Sakit (104), seluruh Indonesia (~15 halaman, ~20 detik)
uv run --env-file ../.env python scripts/sync_facilities.py

# Satu provinsi saja (mis. 31 = DKI Jakarta) — jauh lebih cepat
uv run --env-file ../.env python scripts/sync_facilities.py --province 31

# Ikut menyertakan Apotek (105). Dipakai cron Railway, demi rute HIJAU.
uv run --env-file ../.env python scripts/sync_facilities.py --include-apotek
```

Cron `facility-sync` di Railway menjalankan `--include-apotek` (lihat [deployment-railway.md §14](../deployment-railway.md)). Konsekuensinya: mirror membengkak dari ~13.900 menjadi ~67.000 baris, dan karena hanya **2,1% Apotek** yang berkoordinat, endpoint `/facilities` menerima `?with_coords=true` agar baris tanpa koordinat tidak perlu diambil saat mengurutkan jarak. Rute HIJAU tetap jatuh ke Puskesmas bila tak ada Apotek berkoordinat di sekitar pasien.

**Nomor WhatsApp dikurasi manual.** MSI tidak punya kolom WhatsApp dan `telp` umumnya nomor rumah/kantor (`021…`). Superuser dapat mengisi nomor WhatsApp per faskes lewat `PUT /api/v1/facilities/{satusehat_id}/whatsapp` (body `{"wa_number": "08123456789"}`, atau `null` untuk menghapus). Nilai ini **tidak ditulis oleh sinkronisasi**, jadi aman terhadap re-sync. Tanpa nomor kurasi, tombol WhatsApp otomatis berganti menjadi tombol "Telepon" memakai `telp`. Pesan WhatsApp diisi otomatis dengan rangkuman skrining pasien (`ScoreResult.summary`, ±450–570 karakter, tanpa nama/NIK/foto), supaya petugas tidak perlu menanyakan ulang; layar MERAH belum punya skor, jadi pesannya kosong.

> **Peringatan:** menjalankan `pytest` **mengosongkan** tabel `facility` — fixture `clean_facilities` menghapus seluruh baris pada setup dan teardown. Jalankan sinkronisasi **setelah** test, sebelum demo, atau endpoint `/facilities` akan mengembalikan daftar kosong.

---

## 5. Jebakan & Temuan Nyata (Jangan Temukan Ulang)

Hal-hal yang dibuktikan langsung lewat panggilan API ke sandbox, bukan sekadar tertulis di dokumentasi:

1. **`limit=2000` gagal di Apigee.** Dokumentasi MSI menyebut batas 2000, tetapi gateway Apigee Kemenkes mengembalikan `502 Bad Gateway` dengan rincian `protocol.http.TooBigBody` ("Body buffer overflow") untuk respon multi-jenis di atas ~1500 baris. Gunakan `limit=1000`.
2. **Kualitas koordinat sangat berbeda antar jenis:**
   - Puskesmas (`102`): **100% berkoordinat**.
   - Rumah Sakit (`104`): **96% berkoordinat**.
   - Apotek (`105`): **hanya 2,1% berkoordinat**.
   - *Angka "92%" di awal riset adalah bias sampling* dari 3 halaman pertama MSI yang didominasi Posyandu (bukan sarana yang dipakai TropiCare). Karena Apotek 98% tanpa koordinat dan menghabiskan 79% ukuran mirror, Apotek dikeluarkan dari sinkronisasi default.
3. **Pencarian NIK ke FHIR `GET /Patient` tidak selalu unik.**
   - Contoh nyata di sandbox: NIK dummy `9271060312000001` mengembalikan `total: 2` (dua catatan pasien berbeda untuk satu NIK). Logika apa pun yang mengasumsikan `entry[0]` akan salah secara acak.
   - Nama pasien selalu disamarkan oleh SATUSEHAT (misal `Ar** Pu**`).
   - Bidang `gender` dan `birthDate` pada data dummy sandbox sering bernilai `None`.
4. **NIK asli warga TIDAK ADA di sandbox.**
   - Kueri NIK penduduk asli ke sandbox selalu mengembalikan `HTTP 200` dengan `total: 0`. Sandbox adalah pangkalan data tiruan terisolasi yang tidak terhubung ke Dukcapil.
   - NIK asli hanya hidup di Production (`api.satusehat.kemkes.go.id`), yang mewajibkan status fasyankes berizin/terverifikasi resmi.
5. **`POST /Patient` TIDAK DIIZINKAN untuk tipe akses mana pun.**
   - Di matriks hak akses SATUSEHAT, `POST /Patient` bernilai `FALSE`. Sistem luar tidak bisa membuat pasien baru — hanya bisa mencari pasien yang sudah didaftarkan faskes/Dukcapil.
6. **Token `expires_in` bernilai string dan berdurasi 4 jam.**
   - Dokumentasi memberi contoh `3599` (angka, 1 jam). Respon asli mengembalikan string `"14399"` (4 jam). Wajib membaca TTL dari badan respon dinamis, bukan mengasumsikan 3600 detik.
7. **Baris tanpa provinsi harus dibuang.**
   - MSI memiliki 17 baris nasional dengan `provinsi.kode` dan `nama` kosong (misalnya data demo seperti `MAKARYO JAYA MERDEKA`). Endpoint `/facilities` mensyaratkan `province`, sehingga baris ini menjadi beban mati jika tersimpan.
8. **Nama DIY tidak seragam.**
   - MSI menamai provinsi kode 34 sebagai `"Yogyakarta"`, sementara front-end TropiCare (`location.ts`) memakai `"Daerah Istimewa Yogyakarta"`. Adapter backend harus menerima kedua nama dan kode numeriknya `"34"`.
9. **Koordinat MSI meleset kilometer, dan sebagian bertentangan dengan provinsinya sendiri.**
   - Satu Puskesmas contoh meleset **3 km** dari lokasi sebenarnya (temuan tim, 15 Okt 2026).
   - Bukan soal pembulatan atau centroid bersama: 44 dari 44 Puskesmas contoh di provinsi 31 punya koordinat **unik**, presisi 4–5 desimal. Nilainya sendiri yang salah.
   - Provinsi pun bisa bertolak. Kueri `kode_provinsi=31 + jenis_sarana=104` mengembalikan 100% baris ber-`provinsi.kode` `31`, tetapi ada baris berkoordinat di Kalimantan (108,49 BT) dan Papua (132,02 BT); 6 rumah sakit berbagi satu koordinat identik. Jangan memakai provinsi turunan koordinat untuk memfilter faskes.
   - **Konsekuensi desain:** koordinat hanya dipakai untuk *mengurutkan*; tautan "Rute" mencari **nama faskes + kota** (`routeURL` di `frontend/src/features/triage/links.ts`), supaya Google Maps yang menyelesaikan nama ke tempat nyata. Mematok titik koordinat akan mengantar pasien ke tempat yang salah.
   - **Tidak ada sumber pengganti yang memadai.** OSM/HOT ("Health Facilities of Indonesia", GeoJSON 2,0 MB, 18.854 fitur) hanya punya 3.677 fitur ber-nama Puskesmas vs 10.462 Puskesmas MSI — kecocokan nama **20%**. Google Geocoding dibatasi ToS-nya (lat/lng hanya boleh di-cache maksimum 30 hari, jadi tidak boleh menjadi mirror), dan Nominatim publik melarang geocoding massal (maksimum 1 permintaan/detik). Perbaikan permanen berarti kurasi manual per faskes (pola `wa_number`) atau laporan ke Kemenkes.
   - Angka di atas diambil dari sandbox (`SATUSEHAT_ENV=sandbox`) pada 15 Okt 2026. Sandbox menyajikan data master nasional yang sama dengan Production — baris contoh `PASRUJAMBE` membawa 7 identifier (sisdmk, bpjs_sarana, pusdatin baru/lama/KMK 2022, satset, dto_msfi) — jadi ini bukan artefak data tiruan.
