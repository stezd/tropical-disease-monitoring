# Acuan Medis TropiCare

Satu-satunya acuan isi medis aplikasi: pertanyaan, kriteria, rute, peringatan, lab, dan perawatan. Dokumen ini menggabungkan Blueprint dan Jawaban Dokter. Keduanya kini diarsipkan apa adanya di [arsip/Blueprint.md](arsip/Blueprint.md) dan [arsip/Jawaban-Dokter.md](arsip/Jawaban-Dokter.md).

**Aturan pakai**

- Kalau JSON konten (`backend/app/triage/content/`) berbeda dengan dokumen ini, **dokumen ini yang berlaku**. Perbaiki JSON-nya, atau perbarui dokumen ini dengan persetujuan DR.
- Teks medis berubah hanya dengan persetujuan **DR**. Bobot dan ambang skor hanya dengan persetujuan **ST**.
- Format masukan dan keluaran Gemma4 ada di [Format-Gemma4.md](Format-Gemma4.md).

**Kode sumber** (di akhir setiap butir)

| Kode | Arti |
| --- | --- |
| `[B-T5]` | Blueprint, Tahap 5 |
| `[J9]` | Jawaban dokter no. 9 |
| `[R1]` | Rekomendasi penyelarasan Blueprint vs jawaban dokter, 14 Okt 2026. Sudah diterapkan, **menunggu OK akhir DR** |
| `[D1]` | Keputusan DR, 15 Okt 2026: gula darah sewaktu, kategori tensi, area sendi di peta nyeri, pemeriksaan opsional |
| `[Tim]` | Keputusan tim di [AGENTS.md](../AGENTS.md) |
| `[Sim]` | Berasal dari simulasi HTML, **belum ditinjau DR** |

**Status:** ✅ disepakati · ⚠️ sumber bertentangan, menunggu DR · ⏳ belum ada isi atau bobot

---

## 1. Keputusan yang masih terbuka

Semua hal yang belum bisa dikerjakan karena menunggu keputusan. Nomor `K…` dirujuk di bagian lain dokumen ini.

### Sudah diputuskan `[R1]`

Sudah jalan di aplikasi. DR tinggal memberi OK akhir.

| No | Keputusan | Alasan singkat |
| --- | --- | --- |
| K1 | Leptospirosis tanpa tanda bahaya → KUNING. Tidak kencing > 6–8 jam, atau mata/kulit sangat kuning saat demam → MERAH. | Fase awal mirip infeksi virus; semua ke IGD = penumpukan. Antibiotik dini (Doksisiklin) cukup di Puskesmas. Oliguria/ikterus = risiko Weil's disease (gagal ginjal akut). |
| K2 | Cacingan → HIJAU (obat cacing apotek). Anak dengan lesu, pucat, atau perut buncit → KUNING. | Anak sering juga malnutrisi/anemia: perlu cek Hb dan Albendazol program dari dokter. |
| K3 | Pasien melihat "Hepatitis Akut". Lab tetap fungsi hati + HBsAg + Anti-HAV IgM. | Hepatitis A yang paling sering tampil akut. Hepatitis B sering diam-diam, tetapi HBsAg tetap SOP FKTP untuk menyingkirkannya. |
| K4 | Varicella + sesak → MERAH. Lenting dekat mata atau bernanah → KUNING + catatan untuk dokter: rujuk segera ke Spesialis Kulit/Mata. | Varicella berkomplikasi bukan kompetensi tuntas Puskesmas (SKDI 4A hanya tanpa komplikasi). Sesak = Pneumonia Varicella. |
| K6–K7 | Teks pop-up NSAID dan obat mampat: versi gabungan (§7). | Pasien perlu tahu larangan, alasan, dan solusinya. |

### Diputuskan DR 15 Okt 2026 `[D1]`

Sudah diterapkan. Patokan dari DR; **teks yang tampil ke pasien/petugas masih perlu OK akhir DR**, dan semuanya **0 poin** sampai ST memberi bobot (K28).

| No | Keputusan | Di aplikasi |
| --- | --- | --- |
| K22a | Gula darah = **gula darah sewaktu (GDS)**, diukur kapan saja tanpa puasa. Patokan **≥ 200 mg/dL = tinggi**. | Label "Gula darah sewaktu" di rangkuman dan fakta Gemma4 (`(≥ 200, tinggi)`); catatan kuning di hasil (teks perlu OK DR, §8). Tidak mengubah skor atau rute. |
| K22b | Tensi sistolik **> 120 dan < 140 = meningkat**. | Kategori tensi di rangkuman dan fakta Gemma4 (§8). Label perlu OK DR. Kenaikan rute > 160 mmHg tidak berubah. |
| K30 | Peta nyeri ditambah **sendi lutut, siku, dan bahu** (kanan/kiri), di **kedua jalur**. | Area baru tanpa bobot. Aturan Chikungunya (pergelangan tangan/kaki) tidak berubah. |
| K31 | Pemeriksaan opsional: **asam urat** dan **kolesterol total** (mg/dL). | Langkah sendiri di jalur kronis, boleh dilewati. Dicatat di rangkuman dan fakta Gemma4, **belum dinilai**: ambang perlu DR (K32), bobot perlu ST (K28). |

### Menunggu DR

| No | Topik | Pilihan / masalah | Di aplikasi sekarang |
| --- | --- | --- | --- |
| K5 | Urutan Peta Ekologi | `[B]` Q2 keluhan → Q3 tanda bahaya → Q4 ekologi · `[J16]` ekologi langsung setelah Q2 | tanda bahaya → keluhan → gejala → ekologi |
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
| K19 | Pertolongan pertama tanda bahaya | Teks `[Sim]` untuk pendarahan, ginjal, napas, otak, dehidrasi; tidak ada untuk krisis hipertensi, koma diabetik, dan mata/kulit sangat kuning | lihat §4 |
| K20 | Nama obat di teks perawatan | Pirantel Pamoat (STH, `[R1]`), Klotrimazol (Tinea), kalamin (Varicella) tidak ada di daftar aman `[J18]` | tetap tampil |
| K21 | ~~Chip foto yang hilang~~ | Tidak berlaku lagi: tahap foto dihapus (keputusan tim, 15 Okt 2026) | — |
| K22 | Ambang lingkar perut | `[B-T6]` menyebut lingkar perut "parameter wajib sindrom metabolik", tanpa angka batas. Gula darah sudah diputuskan (K22a). | dicatat, tidak dinilai |
| K32 | Ambang asam urat dan kolesterol total | Belum ada patokan "tinggi" (misalnya beda laki-laki/perempuan untuk asam urat) | dicatat, tidak dinilai, tanpa label |
| K33 | Teks baru yang perlu OK akhir | Catatan GDS ≥ 200 (`chronic/advice.json` `warnings.glucose_high`); label kategori tensi "normal / meningkat / tinggi / sangat tinggi" (`backend/app/domain/vitals.py`) | sudah tampil |
| K34 | Teks catatan keyakinan rendah (`warnings.low_confidence` di `advice.json`) | Draf: "Perkiraan ini belum cukup meyakinkan ({pct}%). Sebaiknya periksakan ke dokter untuk memastikan." Perlu OK DR untuk teks, dan putusan apakah jalur kronis ikut aturan ini. | ikut di kedua jalur, teks draf |
| K35 | Teks privasi baru (`Privacy.tsx`) | Bagian "Statistik tanpa identitas langsung" (apa yang dicatat dan tidak, tidak bisa dihapus per orang, hanya dibagikan sebagai agregat dengan kelompok < 10 orang disembunyikan), dan penyebutan OpenRouter dan Google sebagai tujuan data model (menggantikan kata "Gemini"). Sebaiknya juga ditinjau ahli hukum sebelum dipakai pasien sungguhan (UU PDP). | teks draf tampil, belum ada OK |

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
| K28 | Bobot proksi suhu dan tensi, tensi (termasuk kategori meningkat/tinggi), gula darah sewaktu, asam urat, kolesterol total, lingkar perut, kehamilan, faktor risiko PTM, dan area sendi baru (lutut, siku, bahu). Sekarang semuanya 0 poin. |
| K29 | Bobot jalur kronis, yang sekarang menyalin angka jalur infeksi. |
| K36 | Nilai `refer_below_pct` = 80 pada persen teratas (`top.pct`), dan `softmax_temperature` (sekarang 20). Persen berasal dari softmax yang sama di kedua mesin. Dari 5 kasus golden, 4 berada di bawah 80 % (65, 51, 65, 60; hanya `systolic_above_160` = 88), jadi hampir semua HIJAU akan naik ke KUNING. ST perlu mengukur dampaknya pada kartu kasus DR. |

---

## 2. Prinsip yang tidak berubah

- Aplikasi memberi **skrining** atau **perkiraan**, bukan diagnosis. Kata "diagnosis" hanya muncul dalam penafian ("bukan diagnosis dokter"). `[Tim]`
- Nama penyakit tidak boleh ada di teks pilihan jawaban, hanya di halaman hasil. `[Tim]`
- Pemeriksaan tanda bahaya, kenaikan rute karena suhu, dan skor rendah → KUNING adalah **aturan tetap**, bukan keluaran model. `[Tim]`
- Rute MERAH: layar tenang, tanpa animasi dan suara, dengan tombol telepon 119 serta nomor 119 dan 112 yang bisa disalin. `[Tim]` `[B-T8]`
- Fitur integrasi di Blueprint belum dibangun (§12). `[Tim]`
- Tidak pernah meminta nama atau foto. Tahap foto dihapus (15 Okt 2026). `[Tim]`

---

## 3. Urutan alur

| Langkah | Isi | Sumber |
| --- | --- | --- |
| Data diri | Siapa yang sakit, usia, jenis kelamin, kehamilan | `[B-T1]` |
| Tahap 1 · Tanda bahaya | 11 kondisi gawat (§4). Satu dipilih → langsung MERAH. | `[B-T3]` |
| Tahap 2 · Keluhan utama | 5 klaster infeksi atau 3 klaster PTM (§5) | `[B-T2]` |
| Tahap 3 · Gejala | Pola gejala dan gejala penyerta per klaster (§5). Gejala penyerta tertentu adalah tanda bahaya → langsung MERAH. | `[B-T5]` `[R1]` |
| Tahap 4 · Ekologi / faktor risiko | Riwayat 1–4 bulan terakhir (§6) | `[B-T4]` |
| Tahap 4 · Riwayat obat | Obat yang diminum + peringatan (§7) | `[B-T4]` |
| Tahap 5 · Pengukuran | Suhu, tensi, gula darah sewaktu, IMT, lingkar perut, proksi (§8) | `[B-T6]` `[D1]` |
| Tahap 5 · Pemeriksaan opsional | Jalur kronis, setelah tensi dan gula darah: asam urat, kolesterol total. Boleh dilewati (§8). | `[D1]` |
| Tahap 5 · Peta nyeri | Bagian tubuh yang sakit + skala nyeri 0–10. **Kedua jalur.** Termasuk sendi lutut, siku, dan bahu. | `[Sim]` `[Tim]` `[D1]` |
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

Dua tanda bahaya juga ditanya lewat gejala penyerta (§5) `[R1]`: mata/kulit sangat kuning saat demam (`kuning`, tidak ada di daftar tahap 1) dan sesak napas pada Varicella (memakai `napas`).

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
| `kuning` | Mata atau kulit sangat kuning saat demam (gejala penyerta klaster Demam) | Leptospirosis berat (Weil's disease), risiko gagal ginjal akut `[R1]` | IGD | ⏳ K19 | ⏳ K19 |

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
| Leptospirosis | Demam naik turun + nyeri/kram betis luar biasa saat ditekan | `[B-T5]` | ✅ Mata/kulit sangat kuning → MERAH `[R1]` |
| Chikungunya | Demam sangat singkat + nyeri sendi melumpuhkan. Nyeri ≥ 7 dan > 90 hari = indikator Chikungunya kronis | `[B-T5]` `[J14]` | ⚠️ K14: aplikasi menulis "Singkat 1–3 hari + ruam merah"; nyeri sendi jadi gejala penyerta. ⏳ K13: durasi tidak ditanya |
| Skistosomiasis | Demam menetap + riwayat gatal berjam-jam setelah berenang di danau | `[B-T5]` | ⚠️ K14: aplikasi menambah "sakit perut" |

Gejala penyerta "mata atau kulit sangat kuning" ditanya untuk semua pola demam. Dipilih → MERAH (`kuning`). `[R1]`

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
| Hepatitis Akut | Kencing warna teh gelap + perut kanan atas sakit | `[B-T5]` | ✅ Tampil "Hepatitis Akut" `[R1]` |
| Cacingan (STH) | **Hanya usia 1–12 tahun:** perut buncit, badan kurus, gatal dubur malam hari, atau keluar cacing saat BAB. Pada dewasa STH lebih tampak sebagai anemia kronis/kelelahan, bukan perut buncit. | `[B-T5]` `[J3]` | ✅ |

Tanda penyerta Cacingan (anak): lesu, pucat, perut buncit. Satu saja → minimal KUNING + catatan petugas "cek Hb, obat cacing program Kemenkes (Albendazol)". `[R1]`

**D · Kulit & mukosa** (Skabies, Tinea, Campak, Varicella, Kusta, Frambusia)

| Perkiraan | Kriteria | Sumber |
| --- | --- | --- |
| Skabies | Gatal luar biasa malam hari di sela jari / lipatan | `[B-T5]` |
| Tinea | Bercak merah/putih bersisik, gatal parah saat berkeringat (ruam cincin) | `[B-T5]` |
| Kusta | Bercak keputihan/merah yang MATI RASA (baal) ditusuk jarum | `[B-T5]` |
| Campak | Ruam merah merata didahului demam, batuk, pilek, mata merah | `[B-T5]` |
| Varicella | Lenting/lepuh air bening menyebar seluruh tubuh | `[B-T5]` |
| Frambusia | Koreng menonjol berlumpur (seperti raspberry), sulit sembuh | `[B-T5]` |

Tanda Varicella berat, ditanya bila pola Varicella dipilih `[J8]` `[R1]`:

- Sesak napas (Pneumonia Varicella) → MERAH (`napas`).
- Lenting dekat mata (risiko Herpes Zoster Ophthalmicus/kebutaan) atau bernanah hijau/kuning (infeksi sekunder) → KUNING + catatan "Peringatan untuk Dokter FKTP: indikasi rujukan segera ke Spesialis Kulit/Mata."

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
| NSAID (Ibuprofen, Aspirin, Asam mefenamat, dll.) | Keluhan Demam | Merah | K6 (di bawah) |
| Obat mampat: Loperamide (Imodium), Attapulgite (Diapet, New Diatabs) `[J13]` | Pola Diare atau Amebiasis | Kuning | K7 (di bawah) |
| Amlodipine | Keluhan Bengkak | Biru | "INFORMASI OBAT: Bengkak di pergelangan kaki/tungkai bawah sering merupakan efek samping vasodilatasi Amlodipine. …" `[B-T4]` · K23 |
| Captopril / ACE inhibitor | Keluhan Napas | Biru | "INFORMASI OBAT: Batuk kering persisten tanpa demam adalah efek samping klasik Captopril akibat akumulasi bradikinin. …" `[B-T4]` · K23 |

Pola teks pop-up: larangan → alasan → solusi. Versi gabungan `[B-T4]` + `[J12]`/`[J13]` `[R1]`:

**K6 · NSAID:** "PERINGATAN KRITIS: Suspek Demam Berdarah (DBD). Hentikan segera penggunaan Aspirin, Ibuprofen, atau Asam Mefenamat! Alasan: pada DBD, obat-obatan ini dapat memicu pendarahan lambung yang fatal. Solusi: turunkan panas HANYA dengan Paracetamol, lakukan kompres hangat, dan perbanyak minum air putih."

**K7 · Obat mampat:** "PERHATIAN: Hentikan obat penghenti mencret (mampat). Jangan gunakan Loperamide, Diapet, atau sejenisnya. Alasan: pada diare berlendir/berdarah (disentri), kuman dan racun harus dikeluarkan lewat BAB, bukan ditahan di dalam perut, agar usus tidak bengkak. Solusi: segera ganti dengan minum Oralit (cegah dehidrasi) dan suplemen Zinc."

Halaman hasil memakai versi ringkas dari teks yang sama (`advice.json`, kolom `result`).

**Obat bebas di halaman hasil** `[J18]`

- Hanya obat berlogo lingkaran hijau/biru Kemenkes. Aman disebut: Paracetamol, Oralit, Zinc, Krim Permethrin 5 % (Skabies), Krim Miconazole (Tinea).
- Dilarang: antibiotik (Amoxicillin, Cefixime) dan antivirus. Obat keras hanya lewat rute KUNING (resep dokter).
- ⏳ K20: nama obat lain yang masih ada di teks perawatan.

---

## 8. Pengukuran mandiri

### Suhu (jalur infeksi) `[B-T6]` `[J1]`

- Suhu dalam °C. Demam = ≥ 38,0 °C (ambang skor, ST).
- Tanpa termometer, tanyakan proksi berikut. "Badan terasa panas" tidak dipakai karena terlalu subjektif `[J1]`.
  - "Apakah demam membuat Anda sampai menggigil gemetar hebat, atau berkeringat deras hingga baju basah kuyup?"
  - "Pegang pergelangan tangan, apakah denyut nadi Anda terasa sangat cepat/berdebar keras saat istirahat?" Takikardia adalah tanda demam tinggi/SIRS. ⏳ K11

### Tensi dan gula darah (jalur kronis) `[B-T6]` `[D1]`

- Tensi sistolik/diastolik (mmHg).
- Tanpa tensimeter, tanyakan proksi berikut:
  - Nadi sangat cepat/berdebar keras saat istirahat.
  - Tengkuk terasa sangat tegang.
- Kategori tensi (label di rangkuman dan fakta Gemma4; tidak mengubah skor) `[D1]`. Label perlu OK DR (K33).

  | Kategori | Patokan |
  | --- | --- |
  | normal | sistolik ≤ 120 |
  | meningkat | sistolik > 120 dan < 140, diastolik < 90 |
  | tinggi | sistolik ≥ 140 atau diastolik ≥ 90 |
  | sangat tinggi | sistolik > 160 (juga menaikkan HIJAU ke KUNING, §9) |

- **Gula darah sewaktu (GDS)**, mg/dL: diukur kapan saja, tidak perlu puasa. **≥ 200 mg/dL = tinggi** `[D1]`.
  - Rangkuman dan fakta Gemma4: `250 mg/dL (≥ 200, tinggi)`.
  - Catatan kuning di hasil (teks perlu OK DR, K33): "Gula darah sewaktu {nilai} mg/dL tergolong **tinggi** (≥ 200 mg/dL). Periksakan gula darah ulang di Puskesmas."
  - Tidak mengubah skor atau rute. Bobot: ST (K28).

### Pemeriksaan opsional (jalur kronis) `[D1]`

- Asam urat (mg/dL, 1–30) dan kolesterol total (mg/dL, 50–600), dari hasil cek terakhir. Boleh dilewati.
- Dicatat di rangkuman/QR dan fakta Gemma4, **belum dinilai**: ambang perlu DR (K32), bobot perlu ST (K28).

### Antropometri `[B-T6]` `[J2]` `[J4]`

- Tinggi (cm) dan berat (kg) → IMT. **Kurus: IMT < 18,5. Obesitas: IMT ≥ 27** (pedoman Kemenkes untuk populasi Indonesia) `[J4]`.
- Lingkar perut (cm), hanya jalur kronis. ⏳ K22: ambang.
- Tanpa timbangan, tanyakan proksi:
  - "Pakaian/celana sangat longgar dalam 1–2 bulan terakhir". Instrumen yang cukup kuat untuk penurunan BB tak disengaja > 5 % pada suspek TBC, HIV, malnutrisi `[J4]`; juga prediktor STH dan DM katabolik `[B-T6]`.
  - "Celana makin sempit di perut / Kelebihan berat badan". Kata "gemuk" diganti `[J2]`; kata "(Obesitas)" dihapus dari teks pilihan atas persetujuan DR (Okt 2026).
- **Obesitas → risiko malaria berat.** Obesitas adalah faktor risiko komplikasi *P. falciparum* (malaria serebral, ARDS), sesuai WHO dan BMJ Global Health `[J2]`. Juga prediktor hipertensi dan DM `[B-T6]`.

### Foto

Tahap foto dihapus (keputusan tim, 15 Okt 2026). Chip temuan visual `[J17]` `[B-T6]` tidak lagi ditanyakan atau dinilai; daftarnya tetap ada di [arsip/Jawaban-Dokter.md](arsip/Jawaban-Dokter.md) no. 17 bila tahap ini dibangun lagi.

---

## 9. Aturan rute

Urutan pemeriksaan:

1. **Tanda bahaya** dipilih, di tahap 1 atau lewat gejala penyerta → **MERAH**. Berlaku di browser, tanpa server. `[B-T3]` `[Tim]` `[R1]`
2. **Skor tertinggi di bawah ambang** → "Belum dapat ditentukan" + **KUNING**. `[B]` `[Tim]`
3. Selain itu → rute penyakit dengan skor tertinggi (§10).
4. **Kenaikan rute** (aturan tetap, bukan model):
   - Suhu **≥ 39,5 °C** (hiperpireksia): HIJAU → minimal KUNING, untuk menyingkirkan pneumonia atau sepsis. Berlaku lintas penyakit. `[B-T7]` `[J15]`
   - Tensi sistolik **> 160 mmHg**: HIJAU → minimal KUNING. `[B-T7]`
   - Varicella: lenting dekat mata atau bernanah → minimal KUNING. `[J8]` `[R1]`
   - Cacingan pada anak: lesu, pucat, atau perut buncit → minimal KUNING. `[R1]`
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
| `varicella` | Varicella ringan / berat / sesak | HIJAU / KUNING + catatan rujukan spesialis / MERAH | `[J8]` `[R1]` | ✅ |
| `sth` | Cacingan (STH) | HIJAU; anak lesu/pucat/perut buncit → KUNING | `[B-T8]` `[R1]` | ✅ |
| `dbd` | DBD (fase demam biasa) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `chik` | Chikungunya (fase akut) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `malaria` | Malaria (tanpa letargi) | KUNING | `[B-T8]` `[J9]` | ✅ |
| `tifoid` | Demam Tifoid | KUNING | `[B-T8]` `[J9]` | ✅ |
| `hepa` | Hepatitis Akut | KUNING | `[B-T8]` `[J9]` `[R1]` | ✅ |
| `amoeba` | Amebiasis | KUNING | `[B-T8]` `[J9]` | ✅ |
| `lepto` | Leptospirosis | KUNING; MERAH bila tidak kencing > 6–8 jam atau mata/kulit sangat kuning | `[B-T8]` `[R1]` | ✅ |
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
| `hepa` | Fungsi hati (SGOT/SGPT, bilirubin); HBsAg; Anti-HAV IgM | `[Sim]`; HBsAg tetap untuk menyingkirkan Hepatitis B `[R1]` |
| `skisto` | Pemeriksaan feses (telur Schistosoma) | `[Sim]` |
| `campak` | Pemeriksaan klinis; Serologi Campak IgM | `[Sim]` |
| `kusta` | Uji rasa raba; BTA kerokan kulit | `[Sim]` |
| `frambusia` | RDT Frambusia (serologi cepat) | `[Sim]` |
| `filaria` | Pemeriksaan darah jari malam hari; RDT Filaria | `[Sim]` |
| semua PTM | GDP, Gula Darah 2 Jam PP, Asam Urat, Profil Lipid, Fungsi Ginjal (Ureum/Kreatinin), HbA1c | `[B-T8]` · K18 |

Penyakit rute HIJAU tidak punya daftar lab. Cacingan yang naik ke KUNING mendapat catatan petugas: cek Hb. `[R1]`

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
  - Catatan petugas (rujukan spesialis Varicella, cek Hb Cacingan) tampil di halaman hasil dan di rangkuman. `[R1]`
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

Belum dibangun (keputusan tim) `[Tim]`. Tetap disebut sebagai rencana di proposal.

| Isi Blueprint | Pengganti di aplikasi |
| --- | --- |
| API Mobile JKN untuk antrean `[B-T9]` | Tombol yang hanya membuka aplikasi Mobile JKN |
| Pre-arrival alert ke SIMRS, *pre-notification* faskes, cek stok OAT/MDT `[B-T8]` | Tidak ada. Hanya tautan pencarian Google Maps. |
| Live tracking ambulans, transmisi data ke 119 `[B-T8]` | Tombol telepon 119 + nomor yang bisa disalin |
| Panduan BHD/RJP interaktif `[B-T8]` | Teks pertolongan pertama (DO/DON'T) di §4 |
| "Diagnosis AI" | "Perkiraan" |

### SATUSEHAT (dipertimbangkan, belum dibangun)

- **Dasar hukum:** Permenkes 24/2022 mewajibkan fasyankes memakai rekam medis elektronik yang terhubung ke SATUSEHAT. Kewajiban ini untuk fasyankes. TropiCare bukan fasyankes, jadi integrasi adalah pilihan, bukan syarat aplikasi berjalan.
- **Manfaat yang diharapkan** `[R1]`:
  - Tanpa input ganda: petugas memindai QR, data skrining (keluhan, proksi antropometri, perkiraan) masuk ke SIMPUS.
  - Bahasa data yang sama dengan sistem pemerintah (HL7 FHIR R4), syarat agar bisa diakui Kemenkes (*regulatory sandbox*).
  - Farmakovigilans: riwayat obat (mis. NSAID) terbaca dokter.
- **Sekarang:** QR hanya membuka halaman rangkuman di browser petugas. Tidak ada data yang dikirim. Integrasi butuh akun dan izin dari Kemenkes, serta persetujuan pasien sebelum data dikirim.

Target waktu penanganan di `[B-T8]` (door-to-needle < 30 menit, door-to-balloon/EKG < 10 menit, resusitasi cairan < 15 menit) adalah konteks klinis untuk proposal, bukan fitur aplikasi.
