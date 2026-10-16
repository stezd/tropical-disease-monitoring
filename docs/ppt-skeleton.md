# slides

1. cover
2. problem
3. solution
4. competition comparation matrix
5. core features (more than 1 slide )
6. flow diagram
7. scalability
8. feasibility
9. thanks

# content

## problem

masalah utama
kurangnya pemahaman masyarakat terhadap penyakit infeksius tropis dan penyakit kronis (jangka panjang) menyebabkan terhambatnya penanganan atau bahkan bisa memperparah penyakit

- Pasien demam berdarah yang minum NSAID berisiko perdarahan saluran cerna masif. fase kritis DBD adalah pada hari ke-3 sampai hari ke-7. Jika ditangani tepat waktu, kemungkinan kematian berada di bawah 0.5%.
- Puskesmas dipadati kasus ringan (kompetensi SKDI 4A), antrean panjang, dan administrasi manual, sehingga kasus penting dapat tertunda.
- pada wilayah terpencil, warga dapat mendatangi faskes yang tidak mempunyai stok obat program (seperti obat kusta atau TBC) sehingga membuang-buang waktu dan ongkos

dan masih banyak lagi dampaknya

## solution

Skrining awal yang mudah diakses, berbasis acuan medis, dan mengarahkan pasien ke layanan yang tepat.
Kuesioner adaptif: dimulai dari data diri, lalu pertanyaan menyesuaikan keluhan, gejala, riwayat lingkungan, riwayat obat, dan peta nyeri.

Analisis AI: Gemma4 + RAG menganalisis jawaban berdasarkan literatur medis yang disetujui dokter, lalu memberi satu perkiraan utama dengan skor kecocokan, tiga kemungkinan lain, dan alasan "kenapa aku menebak ini".

- Hasil dan tindak lanjut: jenis penanganan (Darurat, poli program khusus, Puskesmas, atau perawatan mandiri), dilengkapi langkah yang perlu dilakukan, peringatan obat, informasi faskes terdekat, dan QR rangkuman untuk petugas faskes. Hasilnya berupa skrining, bukan diagnosis dokter.

## competition comparation matrix

see Perbandingan-Kompetitor.md

## feasibility

app cost
railway hobby plan : Rp90k/bulan
OpenRouter : Rp180,28k/bulan
domain : Rp25k/bulan
total : Rp295,28k/bulan

monetization : freemium & subcription B2B
dasbor klinik / puskesmas (~Rp250k - 400k per bulan)
skrining karyawan perusahaan di wilayah endermis (~Rp5-6jt)
pemantauan Penderita hipertensi atau diabetes (~Rp15k/bulan)
