# TropiCare

Kuis bergaya permainan untuk skrining penyakit tropis dan penyakit jangka panjang. Hasilnya berupa rute: MERAH (IGD), KUNING KHUSUS (poli program), KUNING (Puskesmas), atau HIJAU (perawatan mandiri).

TropiCare adalah alat skrining, bukan pengganti diagnosis dokter.

- Backend: FastAPI + SQLModel + PostgreSQL (`backend/`)
- Frontend: React + Vite + Tailwind + shadcn/ui (`frontend/`)
- Panduan untuk pengembang dan agen AI: [AGENTS.md](./AGENTS.md)

## Menjalankan di komputer sendiri

### 1. Yang perlu dipasang

| Alat                                                       | Untuk                          |
| ---------------------------------------------------------- | ------------------------------ |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Database PostgreSQL dan Mailpit |
| [uv](https://docs.astral.sh/uv/getting-started/installation/)     | Python dan paket backend       |
| [Bun](https://bun.sh)                                       | Paket dan server frontend      |
| Git (di Windows: [Git for Windows](https://git-scm.com/download/win), sudah termasuk Git Bash) | Kode dan skrip `.sh` |

Python 3.14 tidak perlu dipasang manual. `uv` akan mengunduhnya sendiri.

### 2. Ambil kode

```bash
git clone <url-repo>
cd tropical-disease-monitoring
```

File `.env` (backend) dan `frontend/.env` sudah ada di repo dan berisi nilai bawaan untuk lokal. Tidak perlu diubah untuk mulai.

### 3. Nyalakan database dan Mailpit

Pastikan Docker Desktop sudah berjalan, lalu dari folder utama repo:

```bash
docker compose up -d db mailpit
```

### 4. Jalankan backend

Dari folder `backend/`:

```bash
uv sync                           # pasang paket
uv run bash scripts/prestart.sh   # migrasi database + data awal
uv run fastapi dev                # server di localhost:8000
```

Di Windows, jalankan perintah di atas dari Git Bash. Kalau memakai PowerShell, ganti baris kedua dengan:

```powershell
uv run alembic upgrade head
uv run python app/initial_data.py
```

Biarkan terminal ini tetap terbuka.

### 5. Jalankan frontend

Buka terminal baru. Dari folder utama repo (bukan `frontend/`):

```bash
bun install
bun run dev
```

### 6. Buka aplikasi

| Alamat                        | Isi                                  |
| ----------------------------- | ------------------------------------ |
| <http://localhost:5173>       | Aplikasi TropiCare                    |
| <http://localhost:8000/docs>  | Dokumentasi API (Swagger)            |
| <http://localhost:8025>       | Mailpit, kotak masuk email lokal     |

Akun admin lokal ada di `.env`: `admin@example.com` / `changethis`. Login tidak wajib; tamu bisa mengisi kuis sampai selesai.

## Sehari-hari

Setelah pemasangan pertama, cukup:

```bash
docker compose up -d db mailpit   # folder utama
cd backend && uv run fastapi dev  # terminal 1
bun run dev                       # terminal 2, folder utama
```

Jalankan `uv sync`, `bun install`, atau `prestart.sh` lagi kalau ada perubahan paket atau migrasi baru setelah `git pull`.

| Perintah                           | Dari mana     | Kapan                                           |
| ---------------------------------- | ------------- | ----------------------------------------------- |
| `uv run bash scripts/test.sh`      | `backend/`    | Menjalankan tes backend                         |
| `uv run bash scripts/lint.sh`      | `backend/`    | Cek kode backend                                |
| `bash scripts/generate-client.sh`  | folder utama  | Setelah API atau isi kuis (`backend/app/triage/content/`) berubah |
| `bun run test`                     | folder utama  | Tes frontend (Playwright)                       |
| `docker compose down`              | folder utama  | Mematikan database dan Mailpit                  |

## Kalau ada masalah

- **`port 5432 is already allocated`**: ada PostgreSQL lain yang berjalan. Matikan dulu, atau hentikan container lama dengan `docker compose down`.
- **Backend gagal tersambung ke database**: cek `docker compose ps`. Service `db` harus berstatus `healthy`.
- **Frontend tampil tapi data kuis tidak muncul**: pastikan backend berjalan di <http://localhost:8000>. Tanda bahaya tetap dicek di browser walau server mati.
- **`bash: command not found` di Windows**: jalankan dari Git Bash, atau pakai versi PowerShell di langkah 4.

## Dokumen lain

- [AGENTS.md](./AGENTS.md): struktur kode, aturan yang tidak boleh dilanggar, daftar fitur
- [DESIGN.md](./DESIGN.md): warna, huruf, komponen
- [docs/Acuan-Medis.md](./docs/Acuan-Medis.md): acuan medis (alur kuis, rute, teks) dan keputusan yang masih terbuka
- [docs/Format-Gemma4.md](./docs/Format-Gemma4.md): format masukan dan keluaran Gemma4 (skor teks)
- [development.md](./development.md): menjalankan seluruh aplikasi dengan Docker Compose, pre-commit hooks
- [deployment.md](./deployment.md) dan [deployment-docker-compose.md](./deployment-docker-compose.md): deploy
