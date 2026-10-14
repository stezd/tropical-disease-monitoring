// Privacy notice, shown on /privasi and from the photo step. Keep it in line with
// what the code actually does (store.ts, location.ts, qr.ts, routes/triage.py).

export const PRIVACY_UPDATED = "14 Oktober 2026"

export function PrivacyText() {
  return (
    <div className="privacy">
      <ul className="privacy-key">
        <li>TropiCare adalah skrining awal, bukan diagnosis dokter.</li>
        <li>Kamu bisa memakai TropiCare tanpa akun.</li>
      </ul>

      <h3>1. Data yang dipakai</h3>
      <ul>
        <li>
          <b>Jawaban kuesioner:</b> siapa yang sakit, usia, jenis kelamin,
          keluhan, gejala, riwayat lingkungan, obat, tanda vital, dan bagian
          tubuh yang sakit.
        </li>
        <li>
          <b>Provinsi (opsional):</b> kalau kamu menekan "Pakai lokasiku",
          lokasimu diubah menjadi nama provinsi di perangkatmu sendiri. Titik
          lokasi tidak dikirim dan tidak disimpan.
        </li>
        <li>
          <b>Foto (opsional):</b> hanya setelah kamu menyetujuinya.
        </li>
        <li>
          <b>Akun (opsional):</b> email, nama, dan kata sandi. Kata sandi
          disimpan dalam bentuk acak (hash), bukan teks aslinya.
        </li>
      </ul>

      <h3>2. Ke mana data pergi</h3>
      <ul>
        <li>
          Jawaban dikirim ke server TropiCare sendiri untuk dihitung, lalu
          hasilnya ditampilkan. Tidak dikirim ke pihak lain. Model AI berjalan
          di server kami sendiri.
        </li>
        <li>
          Selama skrining, jawaban disimpan sementara di browser. Menutup tab
          akan menghapusnya.
        </li>
        <li>
          Jawaban disimpan di server hanya kalau kamu menekan{" "}
          <b>"Ya, simpan tanpa nama"</b>. Yang disimpan hanya jawaban dan hasil
          skrining, tanpa nama, email, atau foto. Tim memakainya
          untuk memperbaiki TropiCare.
        </li>
      </ul>

      <h3>3. Foto</h3>
      <ul>
        <li>Kamera baru bisa dibuka setelah kamu menyetujui.</li>
        <li>
          Kalau analisis foto aktif, foto dikirim ke server TropiCare untuk
          dianalisis lalu langsung dibuang. Kalau tidak aktif, foto tetap di
          perangkatmu.
        </li>
        <li>Foto tidak pernah disimpan dan tidak dibagikan.</li>
        <li>Foto hanya bagian yang sakit. Hindari wajah kalau tidak perlu.</li>
      </ul>

      <h3>4. QR rangkuman</h3>
      <ul>
        <li>
          QR berisi jawabanmu dalam kode ringkas, tanpa nama atau foto.
        </li>
        <li>
          Siapa pun yang memindai QR bisa membaca jawabanmu. Tunjukkan hanya ke
          petugas kesehatan.
        </li>
      </ul>

      <h3>5. Tautan ke aplikasi lain</h3>
      <ul>
        <li>
          Tombol Google Maps dan Mobile JKN membuka aplikasi lain. TropiCare
          hanya mengirim kata pencarian (misalnya "puskesmas terdekat"), bukan
          jawabanmu. Aplikasi itu punya kebijakan privasinya sendiri.
        </li>
      </ul>

      <h3>6. Pilihanmu</h3>
      <ul>
        <li>Kamu boleh berhenti kapan saja.</li>
        <li>
          Jawaban yang disimpan tanpa nama tidak bisa dikaitkan lagi dengan
          kamu, jadi tidak bisa dicari atau dihapus per orang.
        </li>
        <li>Akun bisa dihapus sendiri di Pengaturan akun.</li>
      </ul>

      <p className="privacy-date">Terakhir diperbarui: {PRIVACY_UPDATED}</p>
    </div>
  )
}
