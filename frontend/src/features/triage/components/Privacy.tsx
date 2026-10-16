// Privacy notice, shown on /privasi and in the privacy gate before the first
// question. Keep it in line with what the code actually does (store.ts,
// location.ts, nearby.ts, share.ts, qr.ts, routes/triage.py, routes/users.py).
// Perlu OK DR untuk teksnya.

import { USE_SERVER } from "../nearby"

const PRIVACY_UPDATED = "16 Oktober 2026"

export function PrivacyText() {
  return (
    <div className="privacy">
      <ul className="privacy-key">
        <li>TropiCare adalah skrining awal, bukan diagnosis dokter.</li>
        <li>Kamu bisa memakai TropiCare sampai selesai tanpa akun.</li>
        <li>
          Statistik tanpa identitas langsung dicatat untuk melihat tren
          penyakit.
        </li>
      </ul>

      <h3>1. Data yang dipakai</h3>
      <ul>
        <li>
          <b>Jawaban kuesioner:</b> siapa yang sakit, usia, jenis kelamin,
          keluhan, gejala, riwayat lingkungan, obat, tanda vital, hasil cek lab
          (kalau diisi), dan bagian tubuh yang sakit.
        </li>
        <li>
          <b>Lokasi:</b> setelah kamu setuju, TropiCare meminta izin lokasi dari
          browser. Titik lokasi (koordinat) dipakai untuk mencari fasilitas
          kesehatan terdekat dan mengetahui provinsimu.{" "}
          {USE_SERVER
            ? "Koordinat dikirim ke server kami hanya untuk mencari fasilitas kesehatan terdekat, dan tidak disimpan."
            : "Koordinat diproses di perangkatmu, tidak dikirim ke server kami, dan tidak disimpan."}{" "}
          Yang dipakai untuk skrining hanya nama provinsi. Kalau izin ditolak,
          kamu boleh memilih provinsi sendiri atau melewatinya.
        </li>
        <li>
          <b>Akun (opsional):</b> email, nama, dan kata sandi. Kata sandi
          disimpan dalam bentuk acak (hash), bukan teks aslinya. Kalau kamu
          masuk dengan Google, Google mengirim email dan namamu ke TropiCare.
        </li>
      </ul>

      <h3>2. Ke mana data pergi</h3>
      <ul>
        <li>
          Jawaban tanpa identitas (pilihan jawaban, usia, jenis kelamin, dan
          provinsi) dikirim ke server TropiCare dan ke layanan AI pihak ketiga
          (OpenRouter dan Google) untuk dihitung. Nama dan email tidak ikut
          dikirim. Titik lokasi tidak ikut dikirim ke layanan AI.
        </li>
        <li>
          Kami memakai model gratis. Pada model gratis, penyedia layanan bisa
          memakai data yang dikirim untuk memperbaiki produknya.
        </li>
        <li>
          Teks obat yang kamu ketik sendiri tidak ikut dikirim untuk menghitung
          perkiraan. Kalau ada nama obat yang tidak dikenali aplikasi, teks obat
          itu (tanpa jawaban lain) dikirim ke layanan AI hanya untuk mengenali
          jenis obatnya.
        </li>
        <li>
          Selama skrining, jawaban disimpan sementara di browser. Menutup tab
          akan menghapusnya.
        </li>
      </ul>

      <h3>3. Menyimpan riwayat</h3>
      <ul>
        <li>
          Riwayat pribadi disimpan di server hanya kalau kamu sudah masuk akun
          dan menekan <b>"Simpan ke riwayatku"</b>. Statistik tanpa identitas
          langsung (lihat bagian 4) tetap dicatat untuk setiap skrining yang
          selesai, dengan atau tanpa akun.
        </li>
        <li>
          Skrining yang disimpan terhubung ke akunmu. Tim TropiCare bisa
          memakainya untuk memperbaiki aplikasi.
        </li>
        <li>
          Kamu bisa menghapusnya kapan saja di halaman <b>Riwayat skrining</b>,
          atau dengan menghapus akun (semua riwayat ikut terhapus).
        </li>
      </ul>

      <h3>4. Statistik tanpa identitas langsung</h3>
      <ul>
        <li>
          <b>Yang dicatat:</b> kelompok usia, jenis kelamin, provinsi, tanggal,
          pilihan jawaban, kategori tanda vital, dan hasil perkiraan.
        </li>
        <li>
          <b>Yang tidak dicatat:</b> nama, email, akun, usia persis, angka tanda
          vital, teks obat, lokasi atau koordinat, alamat IP, dan jam.
        </li>
        <li>
          <b>Untuk apa:</b> melihat tren penyakit. Data dibagikan ke mitra hanya
          sebagai agregat, dan kelompok yang kurang dari 10 orang disembunyikan.
        </li>
        <li>
          Catatan ini tidak terhubung ke siapa pun, jadi tidak bisa dihapus per
          orang dan tidak ikut terhapus saat akun dihapus.
        </li>
        <li>
          Kami berusaha agar catatan ini tidak menunjuk ke satu orang. Meski
          begitu, gabungan beberapa keterangan (misalnya usia, jenis kelamin,
          provinsi, dan gejala) secara teori masih bisa mengarah ke seseorang.
        </li>
      </ul>

      <h3>5. QR dan WhatsApp</h3>
      <ul>
        <li>
          QR dan tautan rangkuman berisi jawabanmu dalam kode ringkas, tanpa
          nama, NIK, atau titik lokasi. Siapa pun yang membukanya bisa membaca
          jawabanmu. Bagikan hanya ke petugas kesehatan.
        </li>
        <li>
          Tombol "Kirim rangkuman via WhatsApp" hanya membuka WhatsApp dengan
          pesan yang sudah diisi. Kamu sendiri yang memilih untuk mengirimnya.
          Server TropiCare tidak mengirim apa pun.
        </li>
      </ul>

      <h3>6. Tautan ke aplikasi lain</h3>
      <ul>
        <li>
          Tombol Google Maps, WhatsApp, telepon, dan Mobile JKN membuka aplikasi
          lain. Aplikasi itu punya kebijakan privasinya sendiri.
        </li>
      </ul>

      <h3>7. Pilihanmu</h3>
      <ul>
        <li>Kamu boleh berhenti kapan saja.</li>
        <li>Izin lokasi boleh ditolak; skrining tetap berjalan.</li>
        <li>Akun bisa dihapus sendiri di Pengaturan akun.</li>
      </ul>

      <p className="privacy-date">Terakhir diperbarui: {PRIVACY_UPDATED}</p>
    </div>
  )
}
