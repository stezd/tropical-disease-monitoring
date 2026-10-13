# Acuan Medis TropiCare

Satu-satunya acuan isi medis aplikasi: pertanyaan, kriteria, rute, peringatan, lab, dan perawatan. Dokumen ini menggabungkan Blueprint dan Jawaban Dokter. Keduanya kini diarsipkan apa adanya di [arsip/Blueprint.md](arsip/Blueprint.md) dan [arsip/Jawaban-Dokter.md](arsip/Jawaban-Dokter.md).

**Aturan pakai**

- Kalau JSON konten (`backend/app/triage/content/`) berbeda dengan dokumen ini, **dokumen ini yang berlaku**. Perbaiki JSON-nya, atau perbarui dokumen ini dengan persetujuan DR.
- Teks medis berubah hanya dengan persetujuan **DR**. Bobot dan ambang skor hanya dengan persetujuan **ST**.
- Data dan format per tahap untuk model ada di [Alur-Data.md](Alur-Data.md).

**Kode sumber** (di akhir setiap butir)

| Kode | Arti |
| --- | --- |
| `[B-T5]` | Blueprint, Tahap 5 |
| `[J9]` | Jawaban dokter no. 9 |
| `[Tim]` | Keputusan tim di [AGENTS.md](../AGENTS.md) |
| `[Sim]` | Berasal dari simulasi HTML, **belum ditinjau DR** |

**Status:** ✅ disepakati · ⚠️ sumber bertentangan, menunggu DR · ⏳ belum ada isi atau bobot

---

## 1. Keputusan yang masih terbuka

Semua hal yang belum bisa dikerjakan karena menunggu keputusan. Nomor `K…` dirujuk di bagian lain dokumen ini.

### Menunggu DR

| No | Topik | Pilihan / masalah | Di aplikasi sekarang |
| --- | --- | --- | --- |
| K1 | Rute Leptospirosis | `[B-T8]` dini → KUNING, gagal ginjal → MERAH · `[J9]` → MERAH | KUNING; tanda bahaya "tidak kencing" → MERAH |
| K2 | Rute Cacingan (STH) | `[B-T8]` HIJAU (ringan) · `[J9]` KUNING | HIJAU |
| K3 | Cakupan Hepatitis | `[B-T8]` Hepatitis A & B · `[J9]` Hepatitis A saja | "Hepatitis A/B", lab HBsAg + Anti-HAV IgM |
| K4 | Tempat rujukan Varicella berat | `[J8]` KUNING FKRTL/Spesialis · `[B-T8]` KUNING Puskesmas | KUNING, tempat Puskesmas |
| K5 | Urutan Peta Ekologi | `[B]` Q2 keluhan → Q3 tanda bahaya → Q4 ekologi · `[J16]` ekologi langsung setelah Q2 | tanda bahaya → keluhan → gejala → ekologi |
| K6 | Teks pop-up NSAID | versi `[B-T4]` atau `[J12]` (lihat §7) | versi pendek ketiga, bukan keduanya |
| K7 | Teks pop-up obat mampat | versi `[B-T4]` atau `[J13]` (lihat §7) | versi `[B-T4]` |
| K8 | Teks penafian | versi `[B]` atau `[J22]` (lihat §11) | versi ketiga `[Sim]` |
| K9 | Teks "belum dapat ditentukan" | versi `[B]` (lihat §11) | versi `[Sim]` |
| K10 | Usia mulai ditanya hamil | belum ada sumber | 10 tahun |
| K11 | Nadi cepat saat istirahat (proksi) | Apakah ikut menaikkan rute seperti suhu ≥ 39,5 °C? `[J1]` menyebutnya tanda SIRS | tidak menaikkan rute |
| K12 | Batuk tepat 14 hari | ISPA (< 14 hari) atau TBC (> 14 hari)? `[B-T5]` | pilihan "kurang dari / lebih dari 2 minggu" |
| K13 | Chikungunya kronis | `[B-T5]` `[J14]` butuh nyeri ≥ 7 **dan** durasi > 3 bulan; durasi tidak ditanyakan | hanya peringatan dari skala nyeri |
| K14 | Teks pola gejala yang menyimpang dari sumber | lihat §5, tanda ⚠️ | — |
| K15 | Pegal linu / mialgia ringan | `[B-T8]` HIJAU, tidak ada di 20 penyakit `[J9]` | tidak ada |
| K16 | Rute angina stabil | tidak ada di tabel rute `[B-T8]` | KUNING |
| K17 | Lab dan perawatan penyakit lain | Hanya DBD, Malaria, Tifoid, TBC (lab `[J21]`) dan TBC, Skabies (perawatan `[J20]`) yang dari DR | sisanya `[Sim]` (lihat §10) |
| K18 | Lab, perawatan, dan catatan PTM | Lab PTM `[B-T8]` dipakai sama untuk semua; perawatan hanya Gout dan gaya hidup `[B-T8]`; catatan "tensi tidak diukur" belum ditinjau | sama untuk semua penyakit PTM |
| K19 | Pertolongan pertama tanda bahaya | Teks `[Sim]` untuk pendarahan, ginjal, napas, otak, dehidrasi; tidak ada untuk krisis hipertensi dan koma diabetik | lihat §4 |
| K20 | Nama obat di teks perawatan | Albendazol (STH), Klotrimazol (Tinea), kalamin (Varicella) tidak ada di daftar aman `[J18]` | tetap tampil |
| K21 | Chip foto yang hilang | Lidah (Tifoid), terowongan (Skabies), ruam cincin (Tinea) tidak ada lagi sejak chip `[J17]` | tidak dinilai |
| K22 | Ambang lingkar perut dan gula darah | `[B-T6]` menyebut lingkar perut "parameter wajib sindrom metabolik", tanpa angka batas | dicatat, tidak dinilai |

### Menunggu DR + ST

| No | Topik | Masalah |
| --- | --- | --- |
| K23 | Kata "AI" dan "imputasi" | Pop-up Amlodipine/Captopril `[B-T4]`, catatan IMT, dan layar analisis menyebut "AI akan …". Tulis ulang sesuai cara hitung sebenarnya. |
| K24 | Tifoid di klaster Demam | Tifoid hanya punya pilihan di klaster Perut. Perlukah pilihan di klaster Demam? |
| K25 | Validasi silang Tifoid vs DBD | Teks menyebut petekie, tetapi tidak ada pertanyaan tentang petekie. |
| K26 | Skor CVD | Rumus Framingham adaptasi `[B-T7]` (ST) dan batas HIJAU < 5 % (DR + ST) |

### Menunggu ST (bobot)

| No | Topik |
| --- | --- |
| K27 | Bobot provinsi endemis (§6). Daftar provinsi sudah ada `[J10]`. |
| K28 | Bobot proksi suhu dan tensi, tensi, gula darah, lingkar perut, kehamilan, dan faktor risiko PTM. Sekarang semuanya 0 poin. |
| K29 | Bobot jalur kronis, yang sekarang menyalin angka jalur infeksi. |

---

## 2. Prinsip yang tidak berubah

- Aplikasi memberi **skrining** atau **perkiraan**, bukan diagnosis. Kata "diagnosis" hanya muncul dalam penafian ("bukan diagnosis dokter"). `[Tim]`
- Nama penyakit tidak boleh ada di teks pilihan jawaban, hanya di halaman hasil. `[Tim]`
- Pemeriksaan tanda bahaya, kenaikan rute karena suhu, dan skor rendah → KUNING adalah **aturan tetap**, bukan keluaran model. `[Tim]`
- Rute MERAH: layar tenang, tanpa animasi dan suara, dengan tombol telepon 119 serta nomor 119 dan 112 yang bisa disalin. `[Tim]` `[B-T8]`
- Aplikasi berdiri sendiri. Fitur integrasi di Blueprint tidak dibangun (§12). `[Tim]`
- Tidak pernah meminta NIK, nomor BPJS, atau nama. Foto tidak disimpan. `[Tim]`

---

## 3. Urutan alur

| Langkah | Isi | Sumber |
| --- | --- | --- |
| Data diri | Siapa yang sakit, usia, jenis kelamin, kehamilan | `[B-T1]` |
| Tahap 1 · Tanda bahaya | 11 kondisi gawat (§4). Satu dipilih → langsung MERAH. | `[B-T3]` |
| Tahap 2 · Keluhan utama | 5 klaster infeksi atau 3 klaster PTM (§5) | `[B-T2]` |
| Tahap 3 · Gejala | Pola gejala dan gejala penyerta per klaster (§5) | `[B-T5]` |
| Tahap 4 · Ekologi / faktor risiko | Riwayat 1–4 bulan terakhir (§6) | `[B-T4]` |
| Tahap 4 · Riwayat obat | Obat yang diminum + peringatan (§7) | `[B-T4]` |
| Tahap 5 · Pengukuran | Suhu, tensi, gula darah, IMT, lingkar perut, proksi (§8) | `[B-T6]` |
| Tahap 5 · Peta nyeri | Bagian tubuh yang sakit + skala nyeri 0–10. Hanya jalur infeksi. | `[Sim]` `[Tim]` |
| Tahap 5 · Foto | Chip temuan visual (§8) | `[B-T6]` `[J17]` |
| Analisis | Skor + aturan rute (§9) | `[B-T7]` |
| Hasil | Perkiraan, rute, langkah, lab di rangkuman (§10–11) | `[B-T8]` |

⚠️ **K5:** `[J16]` meminta ekologi dipindah tepat setelah keluhan utama, karena lokasi menentukan *pre-test probability*. Urutan ini tidak mengubah skor aturan, karena semua poin dijumlahkan di akhir.

---

## 4. Data diri dan tanda bahaya

### Data diri `[B-T1]`

- Siapa yang sakit: saya sendiri, anak, orang tua/lansia, keluarga lain.
- Usia (tahun), jenis kelamin.
- Status kehamilan: hanya muncul untuk perempuan. ⏳ **K10:** batas usia.
- Anak = usia < 18 tahun (dipakai untuk pertanyaan imunisasi).

### Tanda bahaya `[B-T3]`

Satu saja dipilih → kuesioner berhenti, layar MERAH. Pemeriksaan berjalan di browser, jadi tetap jalan walau server mati. Di jalur kronis, empat tanda bahaya PTM ditampilkan paling atas.

| ID | Kondisi yang ditanyakan | Perkiraan kondisi | Fasilitas | Lakukan (DO) | Jangan (DON'T) |
| --- | --- | --- | --- | --- | --- |
| `syok` | Muntah hebat persisten, atau tangan dan kaki teraba sangat dingin/basah saat demam | Syok Dengue (DSS) | Resusitasi / ICU `[Sim]` | Baringkan dengan kaki ditinggikan `[B-T8]`. Minum oralit bertahap jika pasien sadar `[J19]`. | Beri makan/minum jika pasien mulai mengantuk/penurunan kesadaran (risiko tersedak/aspirasi) `[J19]` |
| `darah` | Pendarahan spontan sulit berhenti (mimisan parah, gusi berdarah, muntah darah, BAB hitam aspal), atau batuk darah jumlah banyak | Pendarahan masif / TBC batuk darah masif | ICU & transfusi darah `[Sim]` | Mimisan: duduk condong ke depan, tekan cuping hidung 10 menit `[Sim]` ⏳ K19 | — |
| `ginjal` | Tidak buang air kecil sama sekali > 6–8 jam terakhir | Gagal ginjal akut (Leptospirosis/Malaria) | Hemodialisa `[Sim]` | Jangan minum obat anti-nyeri sembarangan; segera berangkat `[Sim]` ⏳ K19 | — |
| `napas` | Sesak sangat berat hingga sulit bicara, dada tertarik ke dalam, bibir membiru, atau stridor | Gagal napas / Pneumonia berat / Campak berat `[J6]` | Oksigen & ICU `[Sim]` | Posisikan setengah duduk, longgarkan pakaian `[Sim]` ⏳ K19 | — |
| `otak` | Penurunan kesadaran, mengigau, kejang, atau leher kaku | Ensefalopati / Malaria serebral / Tifoid toksik | ICU `[Sim]` | Saat kejang: miringkan tubuh, jangan masukkan apa pun ke mulut `[Sim]` ⏳ K19 | — |
| `dehidrasi` | Sangat lemas (letargi), mata sangat cekung, anak menangis tanpa air mata | Dehidrasi berat (termasuk Campak berat `[J6]`) | Resusitasi cairan IGD `[Sim]` | Beri oralit sedikit-sedikit tapi sering selama perjalanan `[Sim]` ⏳ K19 | — |
| `rabies` | Luka robek berdarah digigit anjing, kera, atau kucing liar, atau mendadak takut air/cahaya dan air liur menetes terus | Rabies / gigitan hewan penular rabies | Rabies Center (VAR) | Cuci luka gigitan di air mengalir dengan SABUN minimal 15 menit tanpa henti sebelum ke RS `[J19]` `[B-T8]` | — |
| `jantung` | Nyeri dada kiri seperti tertindih benda sangat berat, menjalar ke rahang/lengan kiri/punggung, keringat dingin sebesar biji jagung | Sindrom Koroner Akut (STEMI) | ⏳ K19 | Kepala agak ditinggikan 30° `[B-T8]` | Beri minum/makan bila kesadaran turun/ngantuk (cegah aspirasi) `[B-T8]` |
| `stroke` | Wajah mendadak mencong, bicara pelo, atau lemah separuh badan yang terjadi tiba-tiba hari ini | Stroke akut | ⏳ K19 | Kepala agak ditinggikan 30° `[B-T8]` | Beri minum/makan bila kesadaran turun/ngantuk (cegah aspirasi) `[B-T8]` |
| `krisis_ht` | Nyeri tengkuk sangat ekstrem hingga pandangan mendadak gelap/kabur, atau mimisan deras | Krisis hipertensi | ⏳ K19 | ⏳ K19 | ⏳ K19 |
| `koma_dm` | Penderita kencing manis mendadak pingsan, mengigau, sangat pucat dan gemetar hebat, atau napas berbau buah (aseton) | Koma diabetik (Ketoasidosis / HHS / Hipoglikemia berat) | ⏳ K19 | ⏳ K19 | ⏳ K19 |

Navigasi: tautan pencarian Google Maps ke IGD; RS dengan hemodialisa untuk `ginjal`; Rabies Center untuk `rabies`. `[Tim]`

---

## 5. Keluhan utama dan gejala

Pasien memilih **satu** klaster. Hanya pertanyaan klaster itu yang muncul. `[B-T5]`
Teks yang dilihat pasien ada di `flow.json`, dan harus setia pada kriteria di bawah.

### Jalur infeksi

**A · Demam & seluruh tubuh** (DBD, Malaria, Chikungunya, Leptospirosis, Skistosomiasis) `[B-T2]`

| Perkiraan | Kriteria | Sumber | Catatan |
| --- | --- | --- | --- |
| DBD | Mendadak sangat tinggi, turun hari ke-3/4 tapi lemas (saddleback) + nyeri belakang bola mata | `[B-T5]` | Nyeri mata ditanya sebagai gejala penyerta |
| Malaria | Demam periodik tiap 2–3 hari + menggigil + keringat dingin deras setelah demam turun | `[B-T5]` | Keringat dingin ditanya sebagai gejala penyerta |
| Leptospirosis | Demam naik turun + nyeri/kram betis luar biasa saat ditekan | `[B-T5]` | ✅ |
| Chikungunya | Demam sangat singkat + nyeri sendi melumpuhkan. Nyeri ≥ 7 dan > 90 hari = indikator Chikungunya kronis | `[B-T5]` `[J14]` | ⚠️ K14: aplikasi menulis "Singkat 1–3 hari + ruam merah"; nyeri sendi jadi gejala penyerta. ⏳ K13: durasi tidak ditanya |
| Skistosomiasis | Demam menetap + riwayat gatal berjam-jam setelah berenang di danau | `[B-T5]` | ⚠️ K14: aplikasi menambah "sakit perut" |

**B · Saluran napas** (ISPA, TBC)

| Perkiraan | Kriteria | Sumber | Catatan |
| --- | --- | --- | --- |
| ISPA | Batuk < 14 hari, hidung tersumbat, tenggorokan gatal | `[B-T5]` | ⏳ K12 |
| TBC | Batuk > 14 hari berturut-turut + keringat malam basah kuyup + tidak nafsu makan | `[B-T5]` | Gejala penyerta di aplikasi: BB turun drastis, keringat malam. ⚠️ K14: "tidak nafsu makan" tidak ditanya |

**C · Pencernaan & perut** (Diare Akut, Tifoid, Amebiasis, Hepatitis, Cacingan)

| Perkiraan | Kriteria | Sumber | Catatan |
| --- | --- | --- | --- |
| Diare akut | Mencret cair > 3x sehari tanpa darah/lendir | `[B-T5]` | ✅ |
| Amebiasis | BAB campur darah/lendir + mulas mengejan sangat perih (tenesmus) | `[B-T5]` | ✅ |
| Demam Tifoid | Pola step-ladder: demam naik perlahan setiap hari seperti anak tangga, memuncak di malam hari + nyeri perut saat disentuh | `[B-T5]` `[J5]` | ✅ · K24 |
| Hepatitis | Kencing warna teh gelap + perut kanan atas sakit | `[B-T5]` | ⚠️ K3 |
| Cacingan (STH) | **Hanya usia 1–12 tahun:** perut buncit, badan kurus, gatal dubur malam hari, atau keluar cacing saat BAB. Pada dewasa STH lebih tampak sebagai anemia kronis/kelelahan, bukan perut buncit. | `[B-T5]` `[J3]` | ✅ |

**D · Kulit & mukosa** (Skabies, Tinea, Campak, Varicella, Kusta, Frambusia)

| Perkiraan | Kriteria | Sumber |
| --- | --- | --- |
| Skabies | Gatal luar biasa malam hari di sela jari / lipatan | `[B-T5]` |
| Tinea | Bercak merah/putih bersisik, gatal parah saat berkeringat (ruam cincin) | `[B-T5]` |
| Kusta | Bercak keputihan/merah yang MATI RASA (baal) ditusuk jarum | `[B-T5]` |
| Campak | Ruam merah merata didahului demam, batuk, pilek, mata merah | `[B-T5]` |
| Varicella | Lenting/lepuh air bening menyebar seluruh tubuh | `[B-T5]` |
| Frambusia | Koreng menonjol berlumpur (seperti raspberry), sulit sembuh | `[B-T5]` |

Tanda Varicella berat, ditanya bila pola Varicella dipilih. Satu saja → rute minimal KUNING `[J8]`:
lenting menyebar hingga dekat mata (risiko Herpes Zoster Ophthalmicus/kebutaan kornea) · sesak napas (Pneumonia Varicella) · cairan lenting berubah jadi nanah hijau/kuning (infeksi sekunder). ⚠️ K4: tempat rujukan.

**E · Pembengkakan kronis** (Filariasis)

| Perkiraan | Kriteria | Sumber |
| --- | --- | --- |
| Filariasis limfatik | Bengkak > 3 bulan, asimetris, menetap meski kaki diangkat, dan bila ditekan jari kulit TIDAK mencekung (non-pitting) | `[B-T5]` `[J7]` |

### Jalur kronis (PTM)

Pasien juga boleh memilih **"tidak ada keluhan"** untuk cek risiko saja. `[Tim]`

| Klaster | Perkiraan | Kriteria | Sumber |
| --- | --- | --- | --- |
| F · Gula & Saraf | DM Tipe 2 | Gejala 3P: mudah lapar, mudah haus, sering kencing malam, **tapi** berat badan turun drastis tanpa sebab | `[B-T5]` |
| F · Gula & Saraf | Neuropati diabetik dini | Sering kesemutan / kebas seperti pakai kaos kaki | `[B-T5]` |
| G · Tekanan & Kepala | Hipertensi, Dislipidemia | Tengkuk leher berat, kaku, memburuk saat lelah | `[B-T5]` |
| G · Tekanan & Kepala | Angina stabil | Nyeri dada/sesak HANYA saat aktivitas (naik tangga), HILANG saat istirahat | `[B-T5]` · ⚠️ K16 |
| H · Sendi | Gout akut | Sendi (terutama jempol kaki) mendadak bengkak, kemerahan, panas, luar biasa nyeri ditekan | `[B-T5]` |

---

## 6. Ekologi dan faktor risiko

Riwayat **1–4 bulan terakhir**. Boleh pilih lebih dari satu. `[B-T4]`

**Jalur infeksi**

| ID | Riwayat | Mengarah ke |
| --- | --- | --- |
| `timur` | Tinggal/baru pulang dari Indonesia Timur (Papua, Maluku, NTT), hutan, atau tambang | Malaria, Frambusia |
| `danau` | Beraktivitas/berenang di Danau Lindu, Napu, atau Bada (Sulawesi Tengah) | Skistosomiasis |
| `banjir` | Lingkungan kebanjiran, atau sering kontak air selokan/lumpur bertikus | Leptospirosis |
| `padat` | Lingkungan sangat padat (asrama, pesantren, panti, permukiman kumuh) | TBC, Skabies, Tinea, Hepatitis A |
| `kontak` | Keluarga serumah batuk lama atau minum obat flek paru 6 bulan | TBC |
| `mr` | Imunisasi MR/Campak anak tidak lengkap (hanya untuk anak) | Campak |

**Jalur kronis**

| ID | Faktor risiko | Mengarah ke |
| --- | --- | --- |
| `keturunan` | Orang tua/saudara kandung dengan kencing manis, darah tinggi, atau stroke di usia muda | DM, Hipertensi, Stroke |
| `rokok` | Merokok aktif atau mantan perokok (> 5 tahun) | Kardiovaskular (juga masuk skor CVD) |
| `metabolik` | Jarang olahraga, rutin makan jeroan, hidangan laut, emping, daging berlemak, atau bersantan | Sindrom metabolik, Gout |

**Provinsi endemis** `[J10]` (sumber: Profil Kesehatan Indonesia, Kemenkes). Provinsi didapat dari lokasi browser atau dipilih pasien, dan hanya nama provinsi yang disimpan. ⏳ K27: bobot.

| Penyakit | Wilayah |
| --- | --- |
| Malaria | Papua, Papua Barat, Maluku, NTT |
| Skistosomiasis | HANYA Sulawesi Tengah (Dataran Tinggi Bada, Napu, Lindu) |
| Kusta | Jawa Timur, Madura, Sulawesi Selatan, Papua |
| Filariasis | NTT, Papua, beberapa kabupaten di Sumatera |

---

## 7. Riwayat obat dan peringatan

Pasien mengetik atau mengetuk obat yang sudah/rutin diminum (opsional). `[B-T4]`

| Pemicu | Syarat | Warna | Teks pop-up |
| --- | --- | --- | --- |
| NSAID (Ibuprofen, Aspirin, Asam mefenamat, dll.) | Keluhan Demam | Merah | ⚠️ **K6**, pilih satu versi (di bawah) |
| Obat mampat: Loperamide (Imodium), Attapulgite (Diapet, New Diatabs) `[J13]` | Pola Diare atau Amebiasis | Kuning | ⚠️ **K7**, pilih satu versi (di bawah) |
| Amlodipine | Keluhan Bengkak | Biru | "INFORMASI OBAT: Bengkak di pergelangan kaki/tungkai bawah sering merupakan efek samping vasodilatasi Amlodipine. …" `[B-T4]` · K23 |
| Captopril / ACE inhibitor | Keluhan Napas | Biru | "INFORMASI OBAT: Batuk kering persisten tanpa demam adalah efek samping klasik Captopril akibat akumulasi bradikinin. …" `[B-T4]` · K23 |

**K6 · NSAID**

- `[B-T4]`: "PERINGATAN KRITIS: Anda terdeteksi berisiko DBD. Hentikan segera penggunaan obat anti-nyeri NSAID. Obat ini memicu pendarahan lambung fatal pada DBD. Gunakan Paracetamol."
- `[J12]`: "PERINGATAN KRITIS: Anda terdeteksi memiliki risiko Demam Berdarah. Hentikan segera penggunaan Aspirin, Ibuprofen, atau obat anti-nyeri NSAID lainnya. Obat ini dapat memicu pendarahan lambung yang fatal. Turunkan panas HANYA dengan Paracetamol dan perbanyak minum air."

**K7 · Obat mampat**

- `[B-T4]`: "PERHATIAN: Hentikan obat penghenti mencret. Infeksi usus butuh dikeluarkan. Ganti dengan Oralit & Zinc."
- `[J13]`: "PERHATIAN: Hentikan obat penghenti mencret. Pada kasus kecurigaan infeksi usus/disentri, kuman harus dikeluarkan dari tubuh, bukan ditahan di dalam perut. Segera ganti dengan ORALIT dan suplemen ZINC."

**Obat bebas di halaman hasil** `[J18]`

- Hanya obat berlogo lingkaran hijau/biru Kemenkes. Aman disebut: Paracetamol, Oralit, Zinc, Krim Permethrin 5 % (Skabies), Krim Miconazole (Tinea).
- Dilarang: antibiotik (Amoxicillin, Cefixime) dan antivirus. Obat keras hanya lewat rute KUNING (resep dokter).
- ⏳ K20: nama obat lain yang masih ada di teks perawatan.

---

## 8. Pengukuran mandiri dan foto

### Suhu (jalur infeksi) `[B-T6]` `[J1]`

- Suhu dalam °C. Demam = ≥ 38,0 °C (ambang skor, ST).
- Tanpa termometer, tanyakan proksi berikut. "Badan terasa panas" tidak dipakai karena terlalu subjektif `[J1]`.
  - "Apakah demam membuat Anda sampai menggigil gemetar hebat, atau berkeringat deras hingga baju basah kuyup?"
  - "Pegang pergelangan tangan, apakah denyut nadi Anda terasa sangat cepat/berdebar keras saat istirahat?" Takikardia adalah tanda demam tinggi/SIRS. ⏳ K11

### Tensi dan gula darah (jalur kronis) `[B-T6]`

- Tensi sistolik/diastolik (mmHg), gula darah (mg/dL).
- Tanpa tensimeter, tanyakan proksi berikut:
  - Nadi sangat cepat/berdebar keras saat istirahat.
  - Tengkuk terasa sangat tegang.
- ⏳ K22: ambang gula darah tidak ada di sumber.

### Antropometri `[B-T6]` `[J2]` `[J4]`

- Tinggi (cm) dan berat (kg) → IMT. **Kurus: IMT < 18,5. Obesitas: IMT ≥ 27** (pedoman Kemenkes untuk populasi Indonesia) `[J4]`.
- Lingkar perut (cm), hanya jalur kronis. ⏳ K22: ambang.
- Tanpa timbangan, tanyakan proksi:
  - "Pakaian/celana sangat longgar dalam 1–2 bulan terakhir". Instrumen yang cukup kuat untuk penurunan BB tak disengaja > 5 % pada suspek TBC, HIV, malnutrisi `[J4]`; juga prediktor STH dan DM katabolik `[B-T6]`.
  - "Celana makin sempit di perut / Kelebihan berat badan (Obesitas)". Kata "gemuk" diganti `[J2]`.
- **Obesitas → risiko malaria berat.** Obesitas adalah faktor risiko komplikasi *P. falciparum* (malaria serebral, ARDS), sesuai WHO dan BMJ Global Health `[J2]`. Juga prediktor hipertensi dan DM `[B-T6]`.

### Foto `[B-T6]` `[J17]`

Foto hanya dianalisis di server sendiri dan tidak disimpan. Sampai analisis foto siap, pasien memilih temuan sendiri. Minta izin dulu. `[Tim]`

| Chip | Mengarah ke | Jalur |
| --- | --- | --- |
| Ruam kemerahan / bintik | Campak, DBD | infeksi `[J17]` |
| Lenting berair / lepuh | Varicella | infeksi `[J17]` |
| Bercak putih mati rasa | Kusta | infeksi `[J17]` |
| Luka borok / bernanah | Frambusia | infeksi `[J17]` |
| Mata kuning / mata merah | Hepatitis (ikterus), Leptospirosis (*conjunctival suffusion*) | infeksi `[J17]` |
| Luka borok / bernanah / menghitam | Ulkus diabetikum (DM) | kronis `[B-T6]` |
| Benjolan keras di sendi | Tofus (Gout kronis) | kronis `[B-T6]` |
| Lipatan leher hitam menebal | Acanthosis nigricans (resistensi insulin, DM) | kronis `[B-T6]` |

⏳ K21: chip yang hilang.

---

## 9. Aturan rute

Urutan pemeriksaan:

1. **Tanda bahaya** dipilih → **MERAH**. Berlaku di browser, tanpa server. `[B-T3]` `[Tim]`
2. **Skor tertinggi di bawah ambang** → "Belum dapat ditentukan" + **KUNING**. `[B]` `[Tim]`
3. Selain itu → rute penyakit dengan skor tertinggi (§10).
4. **Kenaikan rute** (aturan tetap, bukan model):
   - Suhu **≥ 39,5 °C** (hiperpireksia): HIJAU → minimal KUNING, untuk menyingkirkan pneumonia atau sepsis. Berlaku lintas penyakit. `[B-T7]` `[J15]`
   - Tensi sistolik **> 160 mmHg**: HIJAU → minimal KUNING. `[B-T7]`
   - Tanda Varicella berat: minimal KUNING. `[J8]`
   - ⏳ K11: nadi cepat (proksi).
5. **Skor CVD** (jalur kronis): risiko 10 tahun dari usia, lingkar perut, IMT, merokok. Risiko < 5 % → "Risiko PTM rendah", HIJAU. `[B-T7]` ⏳ K26

---

## 10. Perkiraan, rute, lab, dan perawatan

Lab tidak ditampilkan di halaman hasil, hanya di rangkuman dan QR untuk petugas. Lab mengacu pada kompetensi Puskesmas `[J21]`.

### Rute per perkiraan

| ID | Perkiraan | Rute | Sumber | Status |
| --- | --- | --- | --- | --- |
| `ispa` | ISPA ringan | HIJAU | `[B-T8]` `[J9]` | ✅ |
| `diare` | Diare akut (non-dehidrasi) | HIJAU | `[B-T8]` `[J9]` | ✅ |
| `scabies` | Skabies | HIJAU | `[B-T8]` `[J9]` | ✅ |
| `tinea` | Tinea (jamur kulit) | HIJAU | `[B-T8]` `[J9]` | ✅ |
| `varicella` | Varicella ringan / berat | HIJAU / KUNING | `[J8]` `[J9]` | ⚠️ K4 (tempat rujukan berat) |
| `sth` | Cacingan (STH) | HIJAU atau KUNING | `[B-T8]` vs `[J9]` | ⚠️ K2 |
| `dbd` | DBD (fase demam biasa) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `chik` | Chikungunya (fase akut) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `malaria` | Malaria (tanpa letargi) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `tifoid` | Demam Tifoid | KUNING | `[B-T8]` `[J9]` | ✅ |
| `hepa` | Hepatitis A (atau A & B) | KUNING | `[B-T8]` vs `[J9]` | ⚠️ K3 |
| `amoeba` | Amebiasis | KUNING | `[B-T8]` `[J9]` | ✅ |
| `lepto` | Leptospirosis | KUNING (dini) atau MERAH | `[B-T8]` vs `[J9]` | ⚠️ K1 |
| `tbc` | TBC | KUNING KHUSUS (Poli DOTS) | `[B-T8]` `[J9]` | ✅ |
| `kusta` | Kusta | KUNING KHUSUS | `[B-T8]` `[J9]` | ✅ |
| `frambusia` | Frambusia | KUNING KHUSUS | `[B-T8]` `[J9]` | ✅ |
| `filaria` | Filariasis | KUNING KHUSUS | `[B-T8]` `[J9]` | ✅ |
| `skisto` | Skistosomiasis | KUNING KHUSUS | `[B-T8]` `[J9]` | ✅ |
| `campak` | Campak ringan | KUNING KHUSUS (ruang isolasi) | `[J6]` `[J9]` | ✅ Berat → MERAH lewat tanda bahaya `napas`/`dehidrasi` |
| `rabies` | Rabies | MERAH | `[J9]` | ✅ Hanya lewat tanda bahaya, tidak diskor |
| `dm` | DM Tipe 2 stabil | KUNING | `[B-T8]` | ✅ |
| `neuropati` | Neuropati diabetik dini | KUNING | `[B-T8]` | ✅ |
| `hipertensi` | Hipertensi derajat 1–2 | KUNING | `[B-T8]` | ✅ |
| `dislipidemia` | Dislipidemia | KUNING | `[B-T8]` | ✅ |
| `gout` | Gout arthritis | KUNING | `[B-T8]` | ✅ |
| `angina` | Angina stabil | KUNING | — | ⚠️ K16 |

**Kondisi MERAH** `[B-T8]` `[J9]`: Syok Dengue, Malaria serebral, gagal ginjal Leptospirosis, Pneumonia berat / Campak berat, Rabies, TBC batuk darah masif, STEMI, Stroke akut, Krisis hipertensi, Koma diabetik. Semua lewat tanda bahaya (§4).

### Lab untuk rangkuman/QR

| ID | Lab | Sumber |
| --- | --- | --- |
| `dbd` | Darah Rutin (Trombosit/Hematokrit); NS1/IgM/IgG Dengue | `[J21]` |
| `malaria` | Apusan Darah Tebal (Giemsa) / RDT Malaria | `[J21]` |
| `tifoid` | Widal / Tubex TF | `[J21]` |
| `tbc` | Tes Cepat Molekuler (TCM) / BTA Sputum | `[J21]` |
| `amoeba` | Cek feses mikroskopis | `[Sim]`; `[B-T8]` menyebut "Feses" |
| `chik` | Darah lengkap; Serologi Chikungunya (bila tersedia) | `[Sim]` |
| `lepto` | Tes cepat Leptospirosis; Fungsi ginjal (ureum/kreatinin) | `[Sim]` |
| `hepa` | Fungsi hati (SGOT/SGPT, bilirubin); HBsAg; Anti-HAV IgM | `[Sim]` · K3 |
| `skisto` | Pemeriksaan feses (telur Schistosoma) | `[Sim]` |
| `campak` | Pemeriksaan klinis; Serologi Campak IgM | `[Sim]` |
| `kusta` | Uji rasa raba; BTA kerokan kulit | `[Sim]` |
| `frambusia` | RDT Frambusia (serologi cepat) | `[Sim]` |
| `filaria` | Pemeriksaan darah jari malam hari; RDT Filaria | `[Sim]` |
| semua PTM | GDP, Gula Darah 2 Jam PP, Asam Urat, Profil Lipid, Fungsi Ginjal (Ureum/Kreatinin), HbA1c | `[B-T8]` · K18 |

Penyakit rute HIJAU tidak punya daftar lab.

### Perawatan ("Yang perlu dilakukan")

| ID | Teks | Sumber |
| --- | --- | --- |
| `tbc` | Pakai masker medis di dalam rumah, pisahkan alat makan, dan buka jendela kamar agar sinar matahari masuk (kuman TB mati oleh UV). · Pengobatan TBC GRATIS 6 bulan di Poli DOTS. | `[J20]` · kalimat kedua `[Sim]` |
| `scabies` | Cuci semua sprei, selimut, dan handuk dengan air panas. Jemur kasur di bawah terik matahari. · Seluruh anggota keluarga serumah HARUS diobati bersamaan. · Krim Permethrin 5 % dioles seluruh tubuh malam hari. | `[J20]` · Permethrin `[J18]` |
| `rabies` | Cuci luka gigitan di air mengalir dengan SABUN minimal 15 menit tanpa henti. | `[J19]` |
| `gout` | Kompres es, DILARANG memijat sendi bengkak. | `[B-T8]` |
| `dbd` | `[B-T8]`: Perbanyak cairan isotonik/oralit 2–3 liter/hari. Aplikasi memakai teks `[Sim]`: minum banyak cairan; Paracetamol, hindari Ibuprofen/Aspirin; waspadai fase kritis hari ke-3–5. | ⚠️ K17 |
| PTM lain | Batasi garam 1 sdt/hari, gula < 4 sdm/hari, olahraga 150 menit/minggu. | `[B-T8]` · K18 |
| ISPA (HIJAU) | `[B-T8]`: Buka jendela pagi hari & etika batuk. | `[B-T8]` |
| Lainnya | Teks di `diseases.json` | `[Sim]` · K17 |

### Petunjuk per rute `[B-T8]` `[J18]`

- **HIJAU:** edukasi sanitasi dan gaya hidup. Navigasi ke apotek. Hanya obat bebas (§7), tanpa antibiotik.
- **KUNING:** Puskesmas / Klinik Pratama. Tunjukkan QR rangkuman ke petugas.
  - Khusus PTM, peringatan kuning: "INSTRUKSI LAB: Anda DIWAJIBKAN BERPUASA (hanya minum air putih) selama 10–12 jam mulai malam ini sebelum tiba di Puskesmas besok pagi."
- **KUNING KHUSUS:** Puskesmas dengan program nasional (Poli DOTS / eradikasi NTD).
  - TBC: Poli DOTS (TCM).
  - Campak: ruang isolasi `[J6]`.
- **MERAH:** IGD (§4).
- Semua rute: tombol Mobile JKN hanya membuka aplikasinya. `[Tim]`

---

## 11. Teks wajib di halaman hasil

**Penafian** (wajib di setiap halaman hasil). ⚠️ **K8**, pilih satu versi:

- `[B]`: "Peringatan: Aplikasi ini adalah alat bantu triase awal berbasis kecerdasan buatan, antropometri klinis, dan pemetaan risiko spasial-gaya hidup. Hasil ini BUKAN merupakan diagnosis medis final dan BUKAN pengganti pemeriksaan fisik serta laboratorium oleh Dokter di fasilitas kesehatan formal."
- `[J22]`: "Peringatan: Aplikasi ini adalah alat bantu triase awal berbasis AI dan pemetaan epidemiologi. Hasil ini BUKAN merupakan diagnosis medis final dan tidak menggantikan pemeriksaan langsung oleh Dokter."
- Aplikasi `[Sim]`: "Ini adalah skrining awal, bukan diagnosis dokter. Jika kondisi memburuk, segera ke fasilitas kesehatan atau hubungi 119."

**Skor rendah.** ⚠️ **K9**, pilih satu versi:

- `[B]`: "Gejala Anda saat ini belum memenuhi pola spesifik infeksi tropis/metabolik dalam sistem kami. Jika keluhan berlanjut > 3 hari, tetap disarankan berkonsultasi dengan dokter."
- Aplikasi `[Sim]`: "Belum dapat ditentukan. Gejalamu belum cocok dengan satu pola. Lebih aman diperiksa langsung, ya!"

**Kasus uji untuk pitching** `[J11]`: Pemuda 22 tahun pulang KKN di pedalaman Papua 2 minggu lalu. Demam menggigil tiap 2 hari, keringat dingin, baju terasa sangat longgar. Sekarang mulai meracau dan lemas. Hasil yang diharapkan: tanda bahaya `otak` → MERAH, navigasi ke IGD (suspek Malaria serebral), tanpa antrean rawat jalan.

---

## 12. Isi Blueprint yang tidak dibangun

Dihapus karena keputusan tim: aplikasi berdiri sendiri, tanpa integrasi yang butuh perjanjian atau izin `[Tim]`. Tetap disebut sebagai rencana di proposal.

| Isi Blueprint | Pengganti di aplikasi |
| --- | --- |
| QR terintegrasi SATUSEHAT / pengisian RME `[B-T8]` `[B-T9]` | QR berisi alamat aplikasi + jawaban terkode. Halaman rangkuman dihitung di browser petugas. |
| API Mobile JKN untuk antrean `[B-T9]` | Tombol yang hanya membuka aplikasi Mobile JKN |
| Pre-arrival alert ke SIMRS, *pre-notification* faskes, cek stok OAT/MDT `[B-T8]` | Tidak ada. Hanya tautan pencarian Google Maps. |
| Live tracking ambulans, transmisi data ke 119 `[B-T8]` | Tombol telepon 119 + nomor yang bisa disalin |
| Panduan BHD/RJP interaktif `[B-T8]` | Teks pertolongan pertama (DO/DON'T) di §4 |
| "Diagnosis AI" | "Perkiraan" |

Target waktu penanganan di `[B-T8]` (door-to-needle < 30 menit, door-to-balloon/EKG < 10 menit, resusitasi cairan < 15 menit) adalah konteks klinis untuk proposal, bukan fitur aplikasi.
