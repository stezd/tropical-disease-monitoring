Landasan Ilmiah, Protokol Klinis, dan Regulasi Sistem Triase Adaptif Infeksi Tropis, NTD, serta Penyakit Tidak Menular
Pengembangan sistem pendukung keputusan klinis (Clinical Decision Support System / CDSS) dan triase mandiri berbasis kecerdasan buatan (Artificial Intelligence / AI) di negara kepulauan beriklim tropis menuntut arsitektur medis yang mampu menangani beban penyakit ganda (double burden of disease). Indonesia menghadapi koeksistensi antara infeksi tropis akut yang ditularkan melalui vektor maupun zoonosis, Penyakit Tropis Terabaikan (Neglected Tropical Diseases / NTD) yang bersifat endemis-lokal, serta lonjakan Penyakit Tidak Menular (PTM) degeneratif. Rancangan Blueprint Aplikasi: Triase Adaptif Infeksi Tropis, NTD & PTM memperlihatkan keselarasan struktural yang sangat kuat dengan pedoman praktik klinis nasional maupun konsensus medis internasional. Kajian ini memetakan bukti ilmiah dari literatur National Center for Biotechnology Information (NCBI / PubMed) beserta nomor DOI resminya, protokol klinis organisasi profesi kedokteran nasional dan internasional, laporan teknis World Health Organization (WHO), serta regulasi resmi Kementerian Kesehatan Republik Indonesia (Kemenkes RI) untuk memvalidasi setiap tahapan arsitektur aplikasi tersebut.
Kerangka Regulasi Nasional dan Arsitektur Gatekeeper Layanan Primer
Secara arsitektural, sistem triase adaptif ini beroperasi dalam suatu siklus tertutup (closed-loop clinical architecture) yang terbagi ke dalam empat lapisan pemrosesan berurutan. Lapisan pertama mencakup penyaringan demografi absolut, klasterisasi keluhan utama, dan penapisan tanda bahaya primer (Red Flags) pada Tahap 1 hingga Tahap 3, yang dilengkapi jalur pintas eskalasi darurat langsung menuju Instalasi Gawat Darurat (IGD) serta layanan ambulans Public Safety Center (PSC) 119. Lapisan kedua memetakan konteks ekologi One Health, keamanan interaksi obat mandiri, dan anamnesis riwayat penyakit sekarang (History of Present Illness / HPI) secara dinamis pada Tahap 4 dan Tahap 5. Lapisan ketiga menjalankan objektivikasi klinis mandiri dan inferensi Edge AI pada Tahap 6 dan Tahap 7 melalui tiga modul paralel, yaitu imputasi proksi antropometri, Computer Vision lesi kulit terkalibrasi Fitzpatrick IV hingga VI, dan kalkulasi skor risiko kardiovaskular regional WHO SEAR-B. Lapisan keempat mendistribusikan luaran klinis pada Tahap 8 dan Tahap 9 ke dalam empat rute layanan berjenjang (Rute Hijau, Rute Kuning, Rute Kuning Khusus, dan Rute Merah) yang terintegrasi secara langsung dengan antrean Mobile JKN serta standar interoperabilitas rekam medis elektronik nasional SATUSEHAT HL7 FHIR R4.
Operasionalisasi arsitektur digital yang menghubungkan penilaian mandiri pasien dengan fasilitas pelayanan kesehatan (fasyankes) ini berpijak pada tiga pilar hukum kesehatan nasional terkini. Pilar pertama adalah Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan (khususnya Pasal 325 dan ketentuan mengenai Transformasi Teknologi Kesehatan), yang memberikan legitimasi hukum atas pemanfaatan teknologi informasi, telemedisin, serta kecerdasan buatan untuk penguatan sistem kesehatan nasional dan kesinambungan perawatan (continuity of care). Dalam peta jalan Digital Transformation Office (DTO) Kemenkes RI, inovasi algoritma triase semacam ini difasilitasi melalui mekanisme Regulatory Sandbox guna menguji keamanan klinis, keandalan algoritma, dan perlindungan hukum bagi pasien maupun tenaga medis sebelum diintegrasikan secara luas ke dalam ekosistem kesehatan nasional.
Pilar kedua adalah Peraturan Menteri Kesehatan (Permenkes) Republik Indonesia Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit (ditetapkan pada 27 Februari 2026 dan mulai berlaku pada 11 Maret 2026, Berita Negara Republik Indonesia Tahun 2026 Nomor 173). Regulasi payung ini mengonsolidasikan tata kelola Penanggulangan Penyakit Menular (Bab II) dan Penanggulangan Penyakit Tidak Menular (Bab III) dalam satu kerangka hukum terpadu. Pada ranah penyakit menular, Pasal 4 ayat (3) mengatur penyakit tular vektor dan binatang pembawa penyakit yang disebabkan oleh parasit, virus, atau bakteri; Pasal 25 memandatkan penemuan kasus secara aktif maupun pasif melalui skrining dan deteksi dini faktor risiko di masyarakat; Pasal 26 menekankan penanganan kasus untuk mencegah disabilitas serta menghapus stigma dan diskriminasi penderita; sedangkan Bagian Kesepuluh mengukuhkan pendekatan Satu Kesehatan (One Health). Pada ranah PTM, Pasal 42 mengatur pembatasan bahan pangan berisiko PTM dan Pasal 43 menetapkan bahwa deteksi dini faktor risiko wajib dilakukan melalui skrining kesehatan yang mencakup anamnesis, pemeriksaan fisik, dan pemeriksaan penunjang. Implikasi hukum yang krusial bagi pengembang aplikasi adalah bahwa Permenkes Nomor 3 Tahun 2026 ini telah mencabut sebagian regulasi NTD terdahulu—yakni mencabut sebagian Permenkes Nomor 11 Tahun 2019 tentang Penanggulangan Kusta (Berita Negara RI Tahun 2019 Nomor 449, kecuali Pasal 4 terkait strategi, Pasal 16, Pasal 26, dan Pasal 28 beserta Lampiran) dan mencabut sebagian Permenkes Nomor 8 Tahun 2017 tentang Eradikasi Frambusia (Berita Negara RI Tahun 2017 Nomor 351, kecuali Pasal 21 beserta Lampiran)—serta mengintegrasikan kebijakan Permenkes Nomor 94 Tahun 2014 tentang Penanggulangan Filariasis ke dalam kerangka penanggulangan penyakit nasional yang baru.
Pilar ketiga yang memvalidasi pembagian rute triase pada aplikasi adalah Keputusan Menteri Kesehatan (Kepmenkes) Republik Indonesia Nomor HK.01.07/MENKES/1186/2022 tentang Panduan Praktik Klinis (PPK) bagi Dokter di Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP). Regulasi ini dirancang untuk mempertajam fungsi gatekeeper layanan primer guna menekan tingginya angka rujukan kasus non-spesialistik ke fasilitas kesehatan rujukan tingkat lanjut (FKRTL). Kepmenkes Nomor HK.01.07/MENKES/1186/2022 mengklasifikasikan pengelolaan penyakit berdasarkan Standar Kompetensi Dokter Indonesia (SKDI) menjadi Tingkat Kemampuan 4A dan 4B (lulusan dokter mampu mendiagnosis dan menatalaksana secara mandiri dan tuntas di FKTP), Tingkat Kemampuan 3A (mampu mendiagnosis klinis dan memberikan terapi pendahuluan pada keadaan bukan gawat darurat sebelum merujuk), Tingkat Kemampuan 3B (mampu mendiagnosis klinis dan memberikan terapi pendahuluan pada keadaan gawat darurat demi menyelamatkan nyawa sebelum merujuk), serta Tingkat Kemampuan 1 dan 2 (mengenali gambaran klinis dan langsung menentukan rujukan yang paling tepat). Pembagian hasil triase aplikasi menjadi Rute Hijau, Rute Kuning, Rute Kuning Khusus, dan Rute Merah secara presisi menerjemahkan matriks kompetensi SKDI dalam Kepmenkes Nomor HK.01.07/MENKES/1186/2022 ke dalam algoritma triase pra-fasilitas.
Validasi Klinis Tahap 1 hingga Tahap 3: Demografi, Keluhan Utama, dan Deteksi Red Flags
Filter Demografi (Tahap 1) dan Pengelompokan Keluhan Utama (Tahap 2)
Penyaringan variabel usia, jenis kelamin, dan status kehamilan (yang muncul secara dinamis apabila jenis kelamin perempuan dipilih) pada Tahap 1 memiliki justifikasi patofisiologis yang esensial dalam pedoman nasional maupun internasional. Dalam Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue pada Dewasa (Kepmenkes Nomor HK.01.07/MENKES/9845/2020) dan PNPK Tata Laksana Infeksi Dengue Anak dan Remaja (Kepmenkes Nomor HK.01.07/MENKES/4636/2021), status kehamilan, usia bayi atau anak, serta komorbiditas diklasifikasikan sebagai kondisi khusus (Group B Dengue) yang mewajibkan pemantauan ketat di rumah sakit meskipun pasien belum menunjukkan warning signs. Literatur obstetri dan infeksi tropis terindeks NCBI PubMed (PMID: 38994458; PMCID: PMC11239217; DOI: 10.61622/rbgo/2024rbgo73 serta tinjauan klinis JAMA oleh Paz-Bailey et al., 2024; DOI: 10.1001/jama.2023.27724) membuktikan bahwa perempuan hamil yang terinfeksi virus dengue mengalami peningkatan risiko progresivitas menuju bentuk penyakit berat (severe dengue), syok hipovolemik, dan kematian maternal-perinatal. Secara mekanistik, produksi sitokin dan kemokin pro-inflamasi pada infeksi dengue tidak hanya meningkatkan permeabilitas kapiler sistemik dan memicu perubahan vaskular plasenta, tetapi juga menstimulasi kontraksi miometrium uterus yang berpotensi mengakibatkan abortus spontan, persalinan prematur, pertumbuhan janin terhambat (fetal growth restriction), kematian janin intrauterin, serta transmisi vertikal virus dengue (DENV). Pada populasi anak di bawah 15 tahun di daerah hiperendemik, DBD lebih sering terjadi akibat infeksi dengue sekunder dengan fenomena antibody-dependent enhancement (ADE), di mana sistem imun gagal menetralisir serotipe virus baru dan justru memicu kebocoran plasma cepat.
Selain pada penyakit infeksi, variabel usia dan jenis kelamin merupakan determinan utama pada stratifikasi penyakit kardiovaskular dan metabolik. Studi epidemiologi berbasis populasi di NCBI PubMed (PMID: 37818312; PMCID: PMC10560824; DOI: 10.1002/hsr2.1614) dan Pedoman Puskesmas Klaster 3 Kemenkes RI menunjukkan bahwa prevalensi hipertensi dan diabetes melitus meningkat secara signifikan pada kelompok usia 40 tahun ke atas (khususnya rentang usia 50 hingga 59 tahun dengan p < 0,01 untuk hipertensi dan p = 0,02 untuk diabetes), disertai perbedaan profil faktor risiko perilaku seperti merokok (p < 0,01) antara laki-laki dan perempuan. Selanjutnya, pengelompokan delapan klaster keluhan utama pada Tahap 2 mengadopsi pendekatan sindromik (syndromic approach) pada PPK Dokter di FKTP (Kepmenkes Nomor HK.01.07/MENKES/1186/2022), yang mengarahkan penelusuran anamnesis dari keluhan utama menuju diferensiasi sistem organ secara terstruktur.
Filter Gawat Darurat / Primary Survey (Tahap 3)
Penempatan deteksi Red Flags pada Tahap 3 sebelum sistem melakukan anamnesis mendalam merupakan implementasi langsung dari prinsip Primary Survey (Airway, Breathing, Circulation, Disability, Exposure / ABCDE) dan pedoman Emergency Triage Assessment and Treatment (ETAT) dari WHO. Setiap indikator kegawatan pada Q3 didukung oleh parameter klinis terukur dari konsensus kedokteran gawat darurat nasional maupun internasional sebagaimana dipetakan pada tabel berikut.
Indikator Red Flag Aplikasi (Q3)
Entitas Klinis & Patofisiologi
Referensi Pedoman Medis Resmi & Artikel Jurnal (DOI)
Parameter Klinis & Ambang Batas Kritis (Bukti NCBI / Kemenkes / WHO)
Ikon Es / Tangan Dingin
Dengue Shock Syndrome (DSS) / Syok Hipovolemik
WHO Dengue Guidelines (2009/2011); PNPK Infeksi Dengue Dewasa (Kepmenkes 9845/2020) & Anak (Kepmenkes 4636/2021); DOI: 10.61622/rbgo/2024rbgo73
Muncul pada fase defervesensi (hari ke-3 s.d. ke-7): muntah persisten, nyeri perut hebat berkelanjutan, ekstremitas distal dingin/lembab, nadi lemah/filiform, waktu pengisian kapiler (CRT) lebih dari 2 detik, tekanan nadi menyempit kurang dari 20 mmHg, peningkatan hematokrit minimal 20%.
Ikon Tetesan Darah
Perdarahan Gastrointestinal Masif / Hemoptisis Masif TBC
PNPK Infeksi Dengue (Kepmenkes 9845/2020); PPK FKTP (Kepmenkes 1186/2022); PMCID: PMC11233874; DOI: 10.1038/s41598-022-18654-2
Perdarahan mukosa spontan, hematemesis (muntah darah), atau melena (BAB hitam aspal) akibat trombositopenia, disfungsi trombosit kualitatif, dan koagulopati (penurunan fibrinogen serta pemanjangan aPTT); atau batuk darah masif akibat erosi arteri bronkialis pada TBC.
Ikon Toilet Disilang
Gagal Ginjal Akut (Acute Kidney Injury / AKI) ec. Leptospirosis (Weil's Disease), Malaria Berat, atau DSS
WHO Guidelines for Malaria; PNPK Penyakit Ginjal Kronik (Kepmenkes 1634/2023); DOI: 10.61622/rbgo/2024rbgo73
Oliguria didefinisikan secara klinis sebagai produksi urin kurang dari 1,5 mL/kg/jam (pada anak/dengue berat) atau kurang dari 0,5 mL/kg/jam selama minimal 6 jam, atau anuria selama 6 hingga 8 jam akibat nekrosis tubular akut hipoperfusi maupun nefrotoksisitas langsung.
Ikon Paru Biru / Sesak
Gagal Napas Akut, Pneumonia Berat, Campak Berat, atau Edema Paru
WHO ETAT & MTBS Kemenkes; PNPK Dengue (Kepmenkes 9845/2020); PMCID: PMC11233874
Retraksi dinding dada bawah (chest indrawing), stridor saat istirahat (obstruksi jalan napas atas/laringotrakeobronkitis campak), sianosis sentral, atau distress napas akibat kebocoran plasma ke rongga pleura/alveoli.
Ikon Otak / Kejang
Ensefalopati Dengue, Malaria Serebral, Meningoensefalitis, atau Tifoid Toksik
PNPK Infeksi Dengue Dewasa (Kepmenkes 9845/2020); PNPK Malaria Kemenkes; PERDOSSI; DOI: 10.61622/rbgo/2024rbgo73
Penurunan kesadaran (letargi, iritabilitas, koma), kejang, paresis, atau kaku kuduk akibat sekuestrasi eritrosit terinfeksi P. falciparum di mikrovaskular serebral, edema serebri, perdarahan intrakranial, atau oklusi pembuluh darah.
Ikon Lemas Ekstrem
Dehidrasi Berat / Syok Hipovolemik Gastroenteritis Akut
WHO Treatment of Diarrhoea; Pedoman Lintas Diare Kemenkes RI; IDAI (Ikatan Dokter Anak Indonesia); AAFP (2022)
Minimal dua dari tanda dehidrasi berat WHO: letargi/tidak sadar, mata sangat cekung, tidak bisa minum atau malas minum, dan turgor kulit perut kembali sangat lambat (2 detik atau lebih).
Ikon Gigitan Hewan
Luka Gigitan Hewan Penular Rabies (GHPR) Kategori III & Ensefalitis Rabies
WHO Expert Consultation on Rabies; Petunjuk Teknis Penatalaksanaan Kasus GHPR Kemenkes RI; Permenkes No. 3 Tahun 2026
Luka gigitan transdermal tunggal atau multipel yang berdarah dari anjing, kera, atau kucing liar (Kategori III WHO memerlukan pencucian luka 15 menit, Vaksin Anti Rabies/VAR, dan Serum Anti Rabies/SAR), atau gejala patognomonik hidrofobia, fotofobia, dan hipersalivasi otonom.
Ikon Jantung Petir
Sindrom Koroner Akut / ST-Elevation Myocardial Infarction (STEMI)
Pedoman Tata Laksana Sindrom Koroner Akut & Hipertensi pada Penyakit Kardiovaskular PERKI (2025); ESC/AHA Guidelines
Angina tipikal berupa rasa tertekan/berat di substernal menjalar ke lengan kiri, leher, rahang, atau punggung lebih dari 20 menit disertai gejala otonom diaforesis (keringat dingin), mual, atau sinkop akibat ketidakseimbangan suplai dan kebutuhan oksigen miokard.
Ikon Wajah Mencong
Stroke Akut (Iskemik atau Hemoragik)
PNPK Tata Laksana Stroke Kemenkes RI; Pedoman PERDOSSI; Pedoman Klaster 3 Kemenkes RI
Defisit neurologis fokal mendadak mengacu pada akronim BE-FAST atau slogan Kemenkes SeGeRa Ke RS (Senyum tidak simetris/mencong, Gerak separuh anggota tubuh melemah tiba-tiba, bicaRa pelo/afasia).
Ikon Kepala Kilat
Krisis Hipertensi (Hipertensi Emergensi) / Ensefalopati Hipertensif
Pedoman Tatalaksana Hipertensi pada Penyakit Kardiovaskular (PERKI, 2025); PNPK Hipertensi Dewasa (Kepmenkes 4634/2021)
Kenaikan tekanan darah ekstrem disertai kerusakan organ target akut (Hypertension-Mediated Organ Damage / HMOD) seperti retinopati/papiledema (pandangan mendadak gelap/kabur), iskemia serebral, atau edema pulmonal akut.
Ikon Pingsan / Buah
Krisis Hiperglikemia (Ketoasidosis Diabetik / KAD & Status Hiperglikemik Hiperosmolar / SHH) serta Hipoglikemia Berat
Pedoman Pengelolaan dan Pencegahan DM Tipe 2 Dewasa (PERKENI, 2024); PNPK DM Tipe 2 Dewasa (2020)
Penurunan kesadaran, agitasi/mengigau, tremor dan pucat diaforetik (neuroglikopenia serta respons adrenergik pada hipoglikemia), atau pernapasan cepat dan dalam (Kussmaul) disertai napas berbau aseton/buah akibat ketonemia pada KAD.

Pemetaan Ekologi One Health dan Sistem Pakar Interaksi Obat pada Tahap 4
Peta Risiko Lingkungan, Spasial, dan Gaya Hidup (Q4)
Integrasi determinan ekologis dan geospasial pada Q4 merupakan keunggulan epidemiologis yang mengoperasionalkan pendekatan One Health (Satu Kesehatan) sebagaimana diamanatkan dalam Permenkes Nomor 3 Tahun 2026 Bagian Kesepuluh. Dalam kedokteran tropis, probabilitas pra-tes (pre-test probability) suatu penyakit infeksi sangat bergantung pada distribusi geografis vektor, hospes perantara, dan reservoar mamalia di lingkungan pasien.
Bukti paling spesifik dari validitas pemetaan spasial ini terlihat pada indikator deteksi Skistosomiasis yang menanyakan riwayat beraktivitas atau berenang di Danau Lindu, Lembah Napu, atau Lembah Bada (Sulawesi Tengah). Berdasarkan laporan resmi WHO Indonesia (25 Juli 2023), artikel jurnal nasional dari Badan Kebijakan Pembangunan Kesehatan (BKPK) Kemenkes RI oleh Widjaja et al. (Buletin Penelitian Kesehatan, 2017; 45(4):215–222; DOI: 10.22435/bpk.v45i4.7570.215-222), studi internasional (Infectious Diseases of Poverty, 2017; 6(1):1–14; DOI: 10.1186/s40249-017-0256-8), serta laporan surveilans resmi Dinas Kesehatan Provinsi Sulawesi Tengah (2019–2024), skistosomiasis (demam keong) di Indonesia disebabkan oleh cacing trematoda darah Schistosoma japonicum dengan hospes perantara keong amfibi Oncomelania hupensis lindoensis. Di seluruh wilayah Republik Indonesia, penyakit ini hanya ditemukan secara endemik di 28 desa yang tersebar di tiga dataran tinggi tersebut, yakni Dataran Tinggi Lindu di Kabupaten Sigi serta Dataran Tinggi Napu dan Dataran Tinggi Bada di Kabupaten Poso. Penelitian pemetaan spasial Kemenkes RI mengidentifikasi sedikitnya 242 daerah fokus keong O. hupensis lindoensis yang tersebar dengan total luas habitat mencapai 1.407.225 m2, umumnya berupa saluran air di perkebunan coklat, mata air yang mengalir ke pemukiman, serta lahan sawah yang tidak diolah lagi, termasuk 14 fokus keong di kawasan Taman Nasional Lore Lindu. Tantangan eradikasi di ketiga lembah ini menegaskan urgensi pendekatan One Health: meskipun prevalensi pada manusia di Dataran Tinggi Napu berhasil ditekan hingga 0,15% (dengan konsentrasi kasus tertinggi di Desa Dodolo dan Kalemago), laju infeksi (infection rate) pada reservoar mamalia liar—khususnya tikus—masih mencapai 16% di Lindu dan 7,3% di Napu (bahkan riset terdahulu mencatat angka 22,7%), ditambah penularan pada hewan ternak masyarakat. Akibatnya, reinfeksi terus berlangsung ketika warga melakukan aktivitas harian seperti mencuci, mandi, mengambil kayu bakar, atau bertani di area fokus keong tersebut.
Demikian pula, penapisan riwayat perjalanan dalam 1 hingga 4 bulan terakhir dari wilayah Indonesia Timur (Papua, Maluku, NTT) atau area hutan dan pertambangan selaras dengan peta endemisitas tinggi malaria serta target kabupaten/kota endemis dalam Permenkes Nomor 8 Tahun 2017 tentang Eradikasi Frambusia (dan Permenkes Nomor 3 Tahun 2026). Pada klaster lingkungan perkotaan dan pemukiman, paparan banjir atau kontak dengan air selokan dan lumpur padat tikus memetakan risiko transmisi spirochaeta Leptospira, sementara hunian padat (asrama, pesantren, panti, pemukiman kumuh) dan kontak serumah dengan penderita batuk kronis atau pasien yang sedang menjalani terapi Obat Anti Tuberkulosis (OAT) 6 bulan berkorelasi langsung dengan transmisi Mycobacterium tuberculosis, Sarcoptes scabiei, infeksi jamur dermatofita, dan virus Hepatitis A sebagaimana divalidasi oleh literatur epidemiologi dermatologi tropis di NCBI (PMCID: PMC10782289; serta Trends in Parasitology, DOI: 10.1016/j.pt.2007.08.007) dan PPK Dokter di FKTP Kemenkes RI (Kepmenkes 1186/2022). Pada dimensi PTM, pengumpulan variabel riwayat keluarga lini pertama, kebiasaan merokok aktif maupun riwayat merokok, sedentari, dan pola diet tinggi purin/lemak jenuh (jeroan, hidangan laut, emping, santan) memenuhi kriteria skrining faktor risiko metabolik dalam Permenkes Nomor 3 Tahun 2026 Pasal 43, Pedoman PERKI (2025), serta Pedoman Gout IRA (2020 & 2024).
Manajemen Obat dan Peringatan Kritis Berbasis Bukti (Q5)
Empat aturan pemicu (AI Triggers) pada Q5 berfungsi sebagai jaring pengaman farmakovigilans untuk mencegah kesalahan medikasi mandiri (self-medication errors) yang mengancam nyawa sekaligus mengeliminasi jebakan diagnostik (diagnostic pitfalls) akibat efek samping obat (Adverse Drug Reactions / ADR). Mekanisme farmakologis dan rujukan ilmiah beserta nomor DOI untuk keempat pemicu tersebut dirangkum dalam tabel berikut.
Trigger AI pada Aplikasi (Q5)
Agen Farmakologi Terkait
Mekanisme Patofisiologis & Bahaya Klinis
Referensi Pedoman Medis & Artikel Jurnal Resmi (Beserta DOI)
Implikasi Algoritma Triase
Trigger AI 1: Suspek DBD + Obat Anti-Nyeri NSAID
Ibuprofen, Aspirin (Asam Asetilsalisilat / ASA), Natrium Diklofenak, Asam Mefenamat
Virus dengue menyebabkan trombositopenia (penurunan trombopoiesis akibat toksisitas sumsum tulang dan peningkatan destruksi perifer), disfungsi trombosit kualitatif, dan koagulopati (penurunan fibrinogen, pemanjangan aPTT). NSAID dan ASA menginhibisi enzim siklooksigenase (COX-1), menghambat agregasi trombosit, dan menekan prostaglandin pelindung mukosa saluran cerna, sehingga memicu perdarahan gastrointestinal masif, ulserasi, perforasi, serta Sindrom Reye pada anak.
WHO & US CDC Dengue Guidelines; PNPK Infeksi Dengue Kemenkes (Kepmenkes 9845/2020 & 4636/2021); NCBI PubMed: PMID 38994458 / PMCID: PMC11239217 (DOI: 10.61622/rbgo/2024rbgo73); PMID 38723714 / PMCID: PMC11233874 (dan DOI: 10.1016/j.ijscr.2013.08.017); Sharp et al., Clin Infect Dis 2021 (DOI: 10.1093/cid/ciaa837); Alam et al., Sci Rep 2022 (DOI: 10.1038/s41598-022-18654-2); Mohiuddin, 2022 (DOI: 10.31586/ujpp.2023.551); PMCID: PMC10090388; PMCID: PMC8389296; NBK542299.
Pop-up Merah (Kontraindikasi Absolut): Menginstruksikan penghentian NSAID/ASA seketika dan menggantinya dengan antipiretik aman (Paracetamol/Acetaminophen) disertai kompres hangat (tepid sponging).
Trigger AI 2: Suspek Diare Akut / Disentri + Obat Antimotilitas
Loperamide, Attapulgite, Kaolin-Pektin, Bismuth subsalicylate
Loperamide (agonis reseptor opioid mu di pleksus mienterikus) menghambat peristaltik propulsif usus. Pada diare infeksius invasif/inflamatorik (Shigella, Salmonella, Campylobacter, C. difficile, Entamoeba histolytica), stasis isi lumen memperpanjang kontak patogen dan toksin dengan epitel mukosa, memicu kolitis amebik fulminan, megakolon toksik (toxic megacolon), necrotizing enterocolitis, dan perforasi kolon. Overdosis atau penggunaan pada anak di bawah 2 tahun juga memicu depresi SSP dan aritmia ventrikel fatal (QTc prolongation & Torsades de Pointes).
WHO Guidelines on Diarrhoea; AAFP Clinical Guidelines (2022); NIH DailyMed (SetID: 1be585e2-ef49-4210-8a2d-22a326e4cc1b); NCBI PubMed: PMID 17241255 (J Travel Med 2007; 14(1):61–62; DOI: 10.1111/j.1708-8305.2006.00095.x); PMCID: PMC4366607; PMCID: PMC7127018; PMCID: PMC12098968; Bookshelf NBK557885.
Pop-up Kuning (Peringatan Keamanan): Menghentikan obat antimotilitas, khususnya bila terdapat demam, tenesmus, atau darah/lendir pada feses, serta mengarahkan pada terapi rehidrasi cairan dan elektrolit (Oralit & Zinc).
Trigger AI 3: Efek Samping Amlodipine vs. Filariasis Limfatik
Amlodipine, Nifedipine (Golongan Dihydropyridine Calcium Channel Blocker / DHP-CCB)
Amlodipine lebih sering memicu edema perifer dibandingkan non-DHP CCB (12,3% vs. 3,1%) atau DHP CCB lipofilik generasi baru, dengan risiko 2,8 kali lebih tinggi pada dosis tinggi dan berdiri lama. Mekanismenya adalah vasodilatasi selektif pada arteriol pre-kapiler tanpa diimbangi vasodilatasi venula post-kapiler, meningkatkan tekanan hidrostatik intrakapiler dan mendorong transudasi cairan ke interstisial pergelangan kaki (bersifat pitting, simetris/bilateral, rata-rata onset 8,3 hingga 10,5 minggu, dan membaik dengan elevasi tungkai atau penghentian CCB). Sebaliknya, Filariasis Limfatik menyebabkan limfedema asimetris, non-pitting (fibrosis/hiperkeratosis), dan menetap lebih dari 3 bulan.
Permenkes No. 94 Tahun 2014 (Filariasis) & Permenkes No. 3 Tahun 2026; PNPK Hipertensi Dewasa (Kepmenkes 4634/2021); Jurnal Internasional & Nasional: Sica DA, J Clin Hypertens 2003 (DOI: 10.1111/j.1524-6175.2003.02402.x); Makani et al., J Hypertens 2011 (DOI: 10.1097/HJH.0b013e3283472643); Liang et al., J Clin Hypertens 2022 (DOI: 10.1111/jch.14436); Largeau et al., Br J Clin Pharmacol 2021 (DOI: 10.1111/bcp.14752); Savage et al., JAMA Intern Med 2020 (DOI: 10.1001/jamainternmed.2019.7087); PLOS One 2026 (DOI: 10.1371/journal.pone.0336659); PMCID: PMC11082315 (DOI: 10.3389/fpsyt.2024.1394813); J Sains Kesehat 2025 (DOI: 10.25026/jsk.v7i3.2460).
Pop-up Biru (Diferensiasi Diagnostik): Mencegah rujukan palsu (false-positive referral) ke Poli Eradikasi NTD Filariasis pada pasien hipertensi yang mengalami edema vasodilatorik akibat Amlodipine, sekaligus mencegah prescribing cascade pemberian diuretik yang tidak perlu, sembari mengarahkan evaluasi penyesuaian regimen antihipertensi (misalnya penurunan dosis atau kombinasi ACEi/ARB yang menurunkan risiko edema sebesar 38%, RR 0,62) di FKTP.
Trigger AI 4: Efek Samping Captopril (ACEi) vs. Tuberkulosis Paru
Captopril, Lisinopril, Ramipril (Golongan Angiotensin-Converting Enzyme Inhibitor / ACEi)
Enzim ACE (kininase II) secara fisiologis mendegradasi bradikinin dan substansi P. Inhibisi ACE oleh Captopril menyebabkan akumulasi bradikinin dan prostaglandin di saluran pernapasan atas dan bronkus, mengiritasi reseptor batuk serat C tanpa mielin, dan menghasilkan batuk kering persisten non-produktif tanpa demam. Di wilayah endemis TBC, batuk akibat ACEi kerap disalahartikan sebagai TBC paru, atau sebaliknya menyamarkan gejala awal TBC.
Petunjuk Teknis Kolaborasi TBC-HIV Kemenkes (2023); PPK Dokter di FKTP (Kepmenkes 1186/2022); NCBI PubMed: PMID 25035451 / PMCID: PMC4112303 (BMJ Case Reports 2014; DOI: 10.1136/bcr-2014-2[span_284](start_span)[span_284](end_span)05462); Bookshelf NBK431051.
Pop-up Biru (Verifikasi Diferensial): Memvalidasi ada tidaknya gejala konstitusional sistemik TBC (demam meriang, keringat malam basah kuyup, anoreksia, penurunan berat badan) dan gejala respiratorik lain (hemoptisis, sesak, nyeri dada) sesuai algoritma 5 Pertanyaan Skrining TBC Kemenkes sebelum menetapkan suspek TBC Paru.

Melampaui keempat pemicu di atas, sintesis literatur anestesiologi dan penyakit dalam di NCBI PubMed (PMID: 38723714; PMCID: PMC11233874; PMCID: PMC8389296; dan Bookshelf NBK542299) mengungkap interaksi klinis tingkat kedua yang sangat krusial ketika seorang pasien dewasa dengan komorbiditas PTM mengalami infeksi dengue akut. Penelitian tersebut membuktikan bahwa meskipun 83,86% klinisi mengetahui kontraindikasi NSAID dan kortikosteroid pada infeksi dengue, hanya 11,21% yang memahami secara utuh mekanisme patofisiologi dan penyesuaian obat komorbid penyertanya. Pada pasien PTM yang terinfeksi dengue, penggunaan rutin Statin (seperti Simvastatin atau Atorvastatin) harus dihentikan sementara selama fase akut karena potensinya meningkatkan kadar enzim transaminase hati (SGOT/SGPT) dan kreatin kinase (CK) yang memperberat hepatopati serta miositis dengue. Selain itu, konsumsi rutin Diuretik (seperti Furosemide atau Hydrochlorothiazide) dan agen antihipertensi lainnya wajib dievaluasi untuk dihentikan sementara apabila pasien memasuki fase kritis kebocoran plasma (plasma leakage) guna mencegah kolaps kardiovaskular dan syok hipovolemik refrakter, sementara Agen Hipoglikemik Oral dan Antikoagulan (seperti Warfarin yang berinteraksi sinergis memicu perdarahan saluran cerna) menuntut pemantauan ketat di fasilitas kesehatan. Mengintegrasikan aturan peringatan tambahan untuk Statin, Diuretik, dan Antikoagulan pada pasien PTM yang mengeluhkan demam akut akan memberikan nilai tambah keselamatan pasien yang luar biasa pada Tahap 4.
Protokol Anamnesis Mendalam Dinamis (Tahap 5) Berdasarkan Pedoman Perhimpunan Dokter
Pada Tahap 5, sistem memunculkan kelompok pertanyaan History of Present Illness (HPI) secara spesifik berdasarkan klaster gejala dan risiko yang teridentifikasi pada tahap sebelumnya. Seluruh deskriptor gejala klinis yang digunakan dalam aplikasi memiliki korespondensi langsung dengan kriteria diagnostik dalam PNPK Kemenkes RI, Panduan Praktik Klinis (PPK) perhimpunan dokter spesialis di bawah naungan Ikatan Dokter Indonesia (IDI) dan Perhimpunan Dokter Spesialis Penyakit Dalam Indonesia (PAPDI), serta pedoman teknis WHO sebagaimana dipetakan pada tabel matriks klinis di bawah ini.
Klaster Anamnesis (Tahap 5)
Entitas Penyakit Target
Karakteristik Klinis Patognomonik pada Blueprint
Dasar Pedoman Klinis Resmi & Artikel Jurnal (DOI)
Klaster 1: Demam Vektor & Zoonosis
DBD, Malaria, Leptospirosis, Chikungunya Kronis, Skistosomiasis
Demam bifasik (saddleback) turun hari ke-3/4 disertai letargi & nyeri retro-orbital (DBD); paroksisme periodik 2–3 hari menggigil-demam-berkeringat (Malaria); nyeri tekan otot betis gastrocnemius (Leptospirosis); artralgia melumpuhkan VAS minimal 7 durasi lebih dari 90 hari (Chikungunya Kronis); swimmer's itch diikuti demam menetap Sindrom Katayama 4–8 minggu kemudian (Skistosomiasis).
PNPK Infeksi Dengue Dewasa (Kepmenkes 9845/2020) & Anak (Kepmenkes 4636/2021); Kriteria WHO 2011; Pedoman Skistosomiasis Dinkes Sulteng & BKPK Kemenkes RI (DOI: 10.22435/bpk.v45i4.7570.215-222 & DOI: 10.1186/s40249-017-0256-8); PMCID: PMC11239217 (DOI: 10.61622/rbgo/2024rbgo73).
Klaster 2: Saluran Napas
ISPA Akut vs. Tuberkulosis (TBC) Paru
Batuk akut kurang dari 14 hari disertai rinitis/faringitis (ISPA) versus batuk produktif/kronis 14 hari atau lebih (2 minggu) disertai diaforesis nokturnal (keringat malam basah kuyup tanpa aktivitas), anoreksia, penurunan berat badan, demam subfebris, atau hemoptisis (TBC Paru).
PPK Dokter di FKTP (Kepmenkes 1186/2022); Petunjuk Teknis Kolaborasi TBC-HIV Kemenkes RI (2023) (Algoritma 5 Pertanyaan: 4 Gejala + 1 Tanda); PNPK TBC Kemenkes & PDPI.
Klaster 3: Pencernaan & Hepatobilier
Diare Akut, Amebiasis, Demam Tifoid, Hepatitis A/B, Cacingan (STH)
Diare cair lebih dari 3 kali/hari tanpa darah/lendir (Diare Akut); disentri darah/lendir disertai tenesmus perih (Amebiasis); pola demam step-ladder memuncak malam hari + nyeri tekan abdomen (Tifoid); bilirubinuria warna teh gelap + nyeri kuadran kanan atas (Hepatitis Akut); malnutrisi kurus-perut buncit + pruritus ani nokturnal/ekspulsi cacing usia 1–12 tahun (STH).
PPK Dokter di FKTP (Kepmenkes 1186/2022); Pedoman Lintas Diare Kemenkes & IDAI; Permenkes No. 15 Tahun 2017 tentang Penanggulangan Cacingan; PMID 17241255 (DOI: 10.1111/j.1708-8305.2006.00095.x).
Klaster 4: Kulit & Lesi Mukosa (NTD & Eksantema)
Skabies, Tinea, Kusta (PB/MB), Campak, Varicella, Frambusia
Pruritus nokturnal sela jari/lipatan (Skabies); plak eritematosa bersisik tepi aktif central clearing gatal saat berkeringat (Tinea); makula hipopigmentasi/eritematosa anestesi/mati rasa tusuk jarum (Kusta); ruam makulopapular didahului prodromal 3C batuk, pilek, konjungtivitis (Campak); vesikel menyebar sentrifugal (Varicella); papiloma/ulkus bergranulasi mirip raspberry (Frambusia).
Permenkes No. 11 Tahun 2019 & PNPK Tatalaksana Kusta (Kepmenkes 308/2019); Permenkes No. 8 Tahun 2017 tentang Eradikasi Frambusia; Permenkes No. 3 Tahun 2026; WHO Skin NTDs Framework (2022) & Int Health 2025 (DOI: 10.1093/inthealth/ihaf068).
Klaster 5: Pembengkakan Kronis NTD
Filariasis Limfatik
Edema ekstremitas bawah yang berlangsung kronis lebih dari 3 bulan, bersifat asimetris, menetap, dan tidak mencekung saat ditekan jari (non-pitting edema) disertai penebalan kulit.
Permenkes No. 94 Tahun 2014 tentang Penanggulangan Filariasis; Permenkes No. 3 Tahun 2026; Moffatt et al., QJM 2003 (DOI: 10.1093/qjmed/hcg126).
Klaster 6: Gula & Saraf PTM
Diabetes Melitus Tipe 2 & Neuropati Diabetik
Trias klasik 3P (Poliuria, Polidipsia, Polifagia) disertai penurunan berat badan katabolik tanpa sebab jelas (DM Tipe 2); parestesia/kesemutan atau hipoestesia/kebas bilateral simetris berpola kaos kaki (stocking-and-glove distribution) (Polineuropati Diabetik).
Pedoman Pengelolaan dan Pencegahan DM Tipe 2 Dewasa di Indonesia (PERKENI, 2024); PNPK Tata Laksana DM Tipe 2 Dewasa (2020); Pedoman Terapi Insulin PERKENI (2021).
Klaster 7: Tekanan & Kepala PTM
Hipertensi Esensial, Dislipidemia, & Angina Pektoris Stabil
Sakit kepala oksipital, tengkuk terasa berat/kaku, berdebar-debar, pusing (Hipertensi); nyeri dada substernal atau sesak napas yang dipicu eksklusif oleh aktivitas fisik (naik tangga) dan mereda dengan istirahat (Angina Pektoris Stabil / PJK).
Pedoman Tatalaksana Hipertensi pada Penyakit Kardiovaskular (PERKI, 2025); PNPK Tata Laksana Hipertensi Dewasa (Kepmenkes 4634/2021); Konsensus InaSH.
Klaster 8: Sendi PTM
Artritis Gout Akut
Serangan inflamasi sendi monoartikular mendadak (khususnya sendi metatarsofalangeal pertama / jempol kaki / podagra) dengan tanda kardinal bengkak, eritema (kemerahan), teraba panas, dan nyeri tekan ekstrem dengan onset mencapai puncak kurang dari 12 hingga 24 jam.
Pedoman Diagnosis dan Tatalaksana Hiperurisemia & Artritis Gout (Perhimpunan Reumatologi Indonesia / IRA, 2020 & Edisi Pembaruan 2024, ISBN: 978-979-3730-48-6).

Dalam mengeksekusi logika anamnesis pada Klaster 1 hingga Klaster 5, ketajaman diferensiasi waktu (temporal profiling) yang dirancang pada blueprint sangat krusial untuk mencegah kesalahan triase. Pada infeksi dengue (Klaster 1), PNPK Infeksi Dengue Dewasa (Kepmenkes Nomor HK.01.07/MENKES/9845/2020) dan PNPK Infeksi Dengue Anak dan Remaja (Kepmenkes Nomor HK.01.07/MENKES/4636/2021) menekankan bahwa perjalanan penyakit memiliki masa inkubasi 4 hingga 10 hari dan terbagi menjadi tiga fase: fase demam (berlangsung 2 hingga 7 hari disertai facial flushing, eritema kulit, mialgia, artralgia, nyeri retro-orbital, serta leukopenia dan penurunan neutrofil menjelang akhir fase demam), fase kritis (terjadi saat penurunan suhu tubuh atau defervescence pada hari ke-3 hingga ke-7 di mana peningkatan permeabilitas kapiler memicu kebocoran plasma dan hemokonsentrasi hematokrit \ge 20\% yang berbanding terbalik dengan kurva trombositopenia), serta fase pemulihan (berlangsung 2 hingga 4 hari saat cairan ekstravaskular direabsorpsi). Identifikasi pola demam pelana kuda (saddleback fever) saat suhu turun di hari ke-3 atau ke-4 namun pasien justru mengalami letargi adalah kunci utama untuk menangkap pasien tepat sebelum jatuh ke dalam syok dengue, yang terbukti menurunkan mortalitas hingga <0,5\%. Demikian pula pada Skistosomiasis, kemampuan algoritma menghubungkan riwayat swimmer's itch (dermatitis serkaria saat serkaria menembus epidermis dan bertransformasi menjadi cacing muda yang bermigrasi melalui jantung dan paru menuju hati) dengan munculnya Sindrom Demam Katayama 4 hingga 8 minggu kemudian (ketika pasangan cacing dewasa berpindah ke pleksus vena mesenterika usus kecil dan mulai meletakkan telur) mencerminkan pemahaman patofisiologi parasitologi yang sangat akurat.
Pada Klaster 4 (Kulit dan Lesi NTD), penggunaan pertanyaan bercak kulit keputihan atau kemerahan yang tidak gatal namun mengalami mati rasa (baal / anestesi) saat diuji tusuk jarum merujuk langsung pada Tanda Kardinal Pertama dalam Permenkes Nomor 11 Tahun 2019 tentang Penanggulangan Kusta dan Kepmenkes Nomor HK.01.07/MENKES/308/2019 tentang PNPK Tatalaksana Kusta. Pedoman Kemenkes menetapkan bahwa kusta didiagnosis apabila ditemukan minimal satu dari tiga tanda kardinal, yaitu: lesi kulit yang kurang rasa atau mati rasa; penebalan saraf tepi yang disertai gangguan fungsi (berupa nyeri saraf tepi, kesemutan, kelemahan motorik anggota gerak atau kelopak mata, kulit tidak berkeringat/anhidrosis, atau rontoknya alis mata/madarosis); atau ditemukannya Basil Tahan Asam (BTA) positif dari pemeriksaan mikroskopis kerokan jaringan kulit. Penemuan dini kusta pada tahap bercak anestesi sebelum munculnya ulkus trofik atau deformitas permanen sangat menentukan keberhasilan pencegahan disabilitas dan penghapusan stigma sosial sebagaimana dimandatkan oleh Permenkes Nomor 3 Tahun 2026 Pasal 26. Sejalan dengan itu, identifikasi koreng menonjol bergranulasi mirip buah raspberry (mother yaw) pada anak atau dewasa di daerah endemis secara tepat menjaring Frambusia stadium primer sesuai Permenkes Nomor 8 Tahun 2017, mengingat bakteri Treponema pallidum subsp. pertenue tidak dapat menembus kulit utuh melainkan masuk melalui luka lecet atau abrasi kulit.
Pada ranah PTM (Klaster 6 hingga Klaster 8), sintesis anamnesis aplikasi juga menunjukkan kesesuaian yang tinggi dengan konsensus perhimpunan profesi subspesialis di Indonesia. Pada Klaster 8, pertanyaan mengenai sendi jempol kaki yang mendadak bengkak, kemerahan, panas, dan sangat nyeri saat disentuh mengacu langsung pada kriteria klinis Podagra dalam Pedoman Diagnosis dan Tatalaksana Hiperurisemia & Artritis Gout yang diterbitkan oleh Perhimpunan Reumatologi Indonesia (IRA) Tahun 2020 dan Edisi Pembaruan Tahun 2024 (ISBN: 978-979-3730-48-6). Pedoman IRA menggarisbawahi bahwa meskipun diagnosis definitif gout ditegakkan melalui penemuan kristal monosodium urate (MSU) pada aspirasi cairan sendi atau tofus, di fasilitas layanan primer keterbatasan sarana mikroskopi polarisasi mengharuskan dokter mengandalkan kriteria klasifikasi klinis berbasis podagra tipikal dan riwayat hiperurisemia. Lebih lanjut, pedoman IRA membedakan secara tegas antara hiperurisemia asimtomatis (yang hanya dikelola melalui modifikasi gaya hidup tanpa pemberian obat penurun asam urat rutin berdasarkan pertimbangan rasio risiko-manfaat) dengan artritis gout akut maupun fase interkritikal/kronis yang membutuhkan intervensi farmakologis terarah.
Objektivikasi Klinis Mandiri, Proksi Antropometri, dan Computer Vision Terkalibrasi Fitzpatrick (Tahap 6 & Tahap 7)
Justifikasi Epidemiologis Proksi Hemodinamik dan Antropometri Berdasarkan Laporan Resmi SKI 2023 (Q6 & Q7)
Tantangan operasional terbesar dalam implementasi tele-triase mandiri di populasi umum Indonesia adalah rendahnya kepemilikan instrumen diagnostik rumah tangga (termometer klinis, sfigmomanometer digital, glukometer kapiler, timbangan berat badan, dan pita antropometri). Data resmi pemerintah dari Laporan Survei Kesehatan Indonesia (SKI) 2023 yang dirujuk dalam Pedoman Kerja Puskesmas Klaster 3 (Kesehatan Usia Dewasa dan Lanjut Usia) Kemenkes RI membuktikan adanya kesenjangan skrining mandiri yang masif: di tingkat nasional, 80,82% penduduk dewasa tidak pernah mengukur lingkar perut, 62,6% tidak pernah memeriksakan kadar gula darah, 61,6% tidak pernah memeriksakan kadar kolesterol, dan 35,61% tidak pernah memantau berat badan. Kesenjangan deteksi dini ini berdampak langsung pada beban morbiditas dan mortalitas nasional, di mana laporan resmi SKI 2023 mencatat bahwa 59,1% disabilitas (gangguan melihat, mendengar, dan berjalan) pada penduduk berusia 15 tahun ke atas disebabkan oleh penyakit yang didapat, dengan 53,5% di antaranya berasal dari PTM (terutama hipertensi dan diabetes melitus), sementara 31,5% mortalitas nasional dikaitkan dengan penyakit serebrovaskular dan jantung, serta prevalensi TBC pada kelompok usia produktif 25 hingga 34 tahun mencapai 0,42%.
Oleh sebab itu, penyediaan opsi proksi hemodinamik pada Q6 (menggigil gemetar hebat / rigors atau keringat basah kuyup sebagai proksi kurva demam tinggi; serta perabaan denyut nadi pergelangan tangan yang cepat/kuat saat istirahat sebagai proksi takikardia) dan proksi antropometri pada Q7 (pakaian atau celana menjadi sangat longgar dalam 1 hingga 2 bulan terakhir sebagai indikator penurunan berat badan drastis / IMT kurang dari 18,5 kg/m2; serta celana terasa makin sempit di pinggang sebagai proksi obesitas sentral) merupakan inovasi biostatistik yang sangat relevan untuk mengatasi hambatan skrining SKI 2023. Ketika diproses oleh algoritma Extreme Gradient Boosting (XGBoost) pada Tahap 7, proksi pakaian longgar secara sahih mewakili status hiperkatabolisme yang meningkatkan probabilitas posterior untuk TBC paru, kecacingan STH, dan DM tipe 2 dekompensata, sedangkan proksi celana sempit mewakili obesitas viseral yang menjadi faktor risiko utama sindrom metabolik, hipertensi, diabetes, serta keparahan klinis malaria Plasmodium falciparum. Dalam pedoman nasional Kepmenkes Nomor HK.01.07/MENKES/4634/2021 dan PERKENI 2024, rentang Indeks Massa Tubuh (IMT) normal untuk populasi dewasa Indonesia ditetapkan pada 18,5 hingga 22,9 kg/m2, dengan ambang batas lingkar pinggang untuk obesitas sentral minimal 90 cm pada laki-laki dan minimal 80 cm pada perempuan.
Computer Vision Terkalibrasi Fitzpatrick untuk NTD Kulit dan Ikterus Sklera (Q8)
Implementasi modul Computer Vision yang dikalibrasi khusus berdasarkan skala tipe kulit Fitzpatrick (Fitzpatrick Skin Type / FST) pada Q8 didukung oleh literatur mutakhir dari WHO Global Neglected Tropical Diseases Programme dan berbagai riset deep learning dermatologi tropis di NCBI PubMed. Berdasarkan studi Global Burden of Disease yang dirujuk di NCBI (PMCID: PMC10782289), penyakit kulit menempati urutan keempat penyebab disabilitas tertinggi non-fatal (Years Lived with Disability / YLDs) secara global setelah anemia defisiensi besi, tuberkulosis, dan gangguan organ indera, namun di negara berkembang rasio dokter terhadap pasien dapat mencapai 1:25.000 dengan kelangkaan ekstrem dokter spesialis dermatologi. Masalah ini diperparah oleh bias algoritmik pada model Convolutional Neural Networks (CNN) konvensional yang dilatih di negara berpendapatan tinggi (High-Income Countries / HIC) menggunakan citra kulit putih (Fitzpatrick I hingga III; lihat juga tinjauan sistematis The Lancet Digital Health, 2022; 4(6):e466–e476; DOI: 10.1016/S2589-7500(22)00023-1), sehingga kinerjanya merosot tajam saat diterapkan pada populasi tropis berkulit sawo matang hingga gelap (Fitzpatrick IV hingga VI) akibat perbedaan kontras optik melanin terhadap eritema dan lesi inflamatorik.
Studi perintis oleh Yotsu et al. (2023) yang dipublikasikan dalam PLOS Neglected Tropical Diseases (2023; 17(8):e0011230; PMID: 37578966; PMCID: PMC10449179; DOI: 10.1371/journal.pntd.0011230; versi pracetak medRxiv PMCID: PMC10055440; DOI: 10.1101/2023.03.14.23287243) memvalidasi penggunaan dua arsitektur deep learning CNN—yakni ResNet-50 dan VGG-16—pada 1.709 citra klinis dari 506 pasien berkulit gelap (Fitzpatrick IV ke atas) untuk mendiagnosis lima penyakit kulit NTD secara simultan, meliputi kusta (leprosy), frambusia (yaws), skabies, ulkus Buruli, dan misetoma. Riset tersebut membuktikan bahwa arsitektur ResNet-50 mengungguli VGG-16 dan mampu memprediksi lebih dari 70% diagnosis secara tepat, dengan akurasi tertinggi dicapai pada ulkus Buruli (88%) dan skabies (85%). Lebih jauh lagi, pelatihan model menggunakan kasus yang terkonfirmasi secara molekuler (PCR) meningkatkan akurasi prediksi sebesar 1% hingga 3% dibandingkan dataset tanpa konfirmasi laboratorium, sementara penghitungan skor ketidakpastian (uncertainty score) membantu menyaring tebakan acak ketika confidence score mendekati 0,200. Temuan ini diperkuat oleh publikasi resmi WHO Global NTD Programme oleh Yotsu, Oiwoh, Mbali, Parajuli, Enbiale, & Ruiz-Postigo (2025) dalam jurnal International Health (2025; 17(5):792–794; PMID: 40590239; PMCID: PMC12406799; DOI: 10.1093/inthealth/ihaf068) yang mengacu pada dokumen kerangka strategis WHO (Ending the neglect to attain the Sustainable Development Goals: a strategic framework for integrated control and management of skin-related neglected tropical diseases, WHO 2022). Dalam studi lapangan terhadap 605 pasien di lima distrik di Kenya menggunakan aplikasi WHO Skin NTDs—yang lebih dari 90% pustaka citranya berasal dari kulit gelap (Fitzpatrick IV hingga VI)—algoritma AI berhasil mencapai sensitivitas klinis sekitar 80% dengan penerimaan kegunaan (usability) yang sangat positif dari petugas kesehatan lini depan.
Meskipun demikian, pengembang aplikasi harus mengantisipasi batas kemampuan visual AI pada presentasi penyakit yang kompleks. Evaluasi independen oleh Deps, Amorim, Repsold, & Almonfrey (2025/2026) (PMID: 42006576; PMCID: PMC13086047; yang juga merujuk konsensus integrasi NTD kulit dalam PLOS Neglected Tropical Diseases, 2023; 17(6):e0011357; DOI: 10.1371/journal.pntd.0011357 dan British Journal of Dermatology; DOI: 10.1093/bjd/ljaf212) terhadap pengklasifikasi visual AI pada aplikasi WHO Skin NTDs menggunakan 423 citra klinis kusta terkonfirmasi lintas spektrum (indeterminate, tuberkuloid, borderline/dimorfik, dan lepromatosa/Virchowian) mengungkap bahwa model AI mencapai Top-5 sensitivity (recall) keseluruhan sebesar 84,9% dan sangat andal pada lesi kusta klasik (87,2%), namun sensitivitasnya turun menjadi 69,6% pada reaksi kusta (reactional states) atau manifestasi atipikal yang bersifat nekrotik, inflamatorik, dan infiltratif. Temuan ini memberikan justifikasi ilmiah mengapa aplikasi tidak boleh hanya mengandalkan citra kamera (Q8), melainkan wajib menggabungkannya secara multimodal dengan anamnesis uji tusuk jarum (mati rasa/baal) pada Tahap 5. Selain itu, dari aspek rekayasa visi komputer, studi di NCBI pada dataset Fitzpatrick 17k (PMCID: PMC12099365) menunjukkan bahwa penerapan algoritma pemisahan piksel latar belakang (background pixel separation) dari piksel lesi kulit mampu mendongkrak akurasi diagnostik pada tugas baru sebesar 43,3% sekaligus memangkas ketimpangan Gini (Gini inequality) antar tipe warna kulit sebesar 20,9% di negara berpendapatan rendah dan menengah (LMIC).
Pada fitur deteksi kelainan mata (ikterus sklera pada Hepatitis A/B vs. conjunctival suffusion atau mata merah tanpa eksudat pada Leptospirosis), validitas penggunaan kamera ponsel cerdas didukung oleh studi Outlaw et al. (2020) di NCBI (PMCID: PMC7051077) yang mengembangkan sistem neoSCB (Scleral-Conjunctival Bilirubinometer). Berbeda dengan kulit yang dipengaruhi oleh konsentrasi melanin epidermis dan pencahayaan latar, sklera dan membran konjungtiva di atasnya memiliki warna dasar putih intrinsik serta mengakumulasi bilirubin sistemik secara langsung, sehingga pencitraan sklera menggunakan kamera ponsel pintar tanpa kartu kalibrasi warna eksternal (colour calibration cards) mampu menyamai performa skrining bilirubinometer transkutan komersial. Berbagai arsitektur pemrosesan citra warna mata dan kulit untuk deteksi ikterus pada orang dewasa maupun neonatus yang dipublikasikan dalam jurnal internasional (Computer Methods in Biomechanics and Biomedical Engineering: Imaging & Visualization, 2023; DOI: 10.1080/21681163.2023.2244601 serta Designs MDPI, 2021; 5(4):63; DOI: 10.3390/designs5040063) mengonfirmasi bahwa analisis kromatisitas digital merupakan metode point-of-care yang objektif, non-invasif, dan berbiaya rendah.

Inferensi Edge AI dan Penyelarasan Skor Risiko Kardiovaskular (Tahap 7)
Pada Tahap 7, mekanisme inferensi backend yang berjalan di dalam perangkat ponsel (Edge AI) mencakup kalkulasi skor risiko penyakit kardiovaskular (CVD) 10 tahun dan aturan validasi silang (cross-validation override). Terkait skor risiko kardiovaskular, blueprint saat ini mencantumkan nomenklatur "CVD Risk Score (Framingham Adaptasi)" yang menghitung risiko serangan jantung atau stroke dalam 10 tahun ke depan berdasarkan Usia, Lingkar Perut, BMI, dan Merokok, lalu menetapkan Rute Hijau apabila skor CVD kurang dari 5%. Evaluasi terhadap regulasi resmi nasional menunjukkan bahwa Kementerian Kesehatan RI—melalui Pedoman Kerja Puskesmas Klaster 3 (Kesehatan Usia Dewasa dan Lanjut Usia), PPK Dokter di FKTP (Kepmenkes Nomor HK.01.07/MENKES/1186/2022), serta Konsensus Penatalaksanaan Hipertensi InaSH—secara resmi telah mengadopsi Tabel Prediksi Risiko PTM yang diadaptasi dari WHO Cardiovascular Disease Risk Charts untuk wilayah epidemiologi SEAR B (South-East Asia Region, yang secara eksplisit mencakup Indonesia, Kamboja, Laos, Sri Lanka, Thailand, Timor-Leste).
Keunggulan fundamental dari WHO Cardiovascular Disease Risk Charts dibandingkan skor Framingham klasik adalah ketersediaan dua versi terkalibrasi sebagaimana divalidasi oleh studi populasi Rezaei et al. (2023) (PMID: 37301218; DOI: 10.1016/S2213-8587(23)00119-5) dan Gujarathi et al. (2025) (National Journal of Community Medicine, 2025; 16(11); DOI: 10.55489/njcm.161120255801), yakni Laboratory-Based Charts (membutuhkan profil kolesterol total dan status diabetes/gula darah puasa) serta Non-Laboratory-Based Charts yang dirancang khusus untuk penapisan awal komunitas ketika hasil pemeriksaan laboratorium belum tersedia. Algoritma Non-Laboratory-Based WHO menghitung estimasi risiko 10 tahun kejadian kardiovaskular fatal maupun non-fatal (infark miokard atau stroke) hanya menggunakan lima variabel input yang seluruhnya telah tersedia pada aplikasi di Tahap 1, Tahap 4, dan Tahap 6: Usia (40 hingga 74 tahun), Jenis Kelamin, Status Merokok, Tekanan Darah Sistolik, dan Indeks Massa Tubuh (IMT/BMI). Selain itu, stratifikasi tingkat risiko pada WHO CVD Risk Charts terbagi atas lima pita risiko: kurang dari 5% (Risiko Sangat Rendah / Hijau), 5% hingga kurang dari 10% (Risiko Rendah), 10% hingga kurang dari 20% (Risiko Sedang), 20% hingga kurang dari 30% (Risiko Tinggi), dan 30% atau lebih (Risiko Sangat Tinggi). Mengingat ambang batas kurang dari 5% untuk Rute Hijau pada Tahap 8 blueprint sudah persis merujuk pada pita risiko terendah WHO CVD Risk Charts, penyempurnaan nomenklatur algoritma pada Tahap 7 menjadi "WHO Non-Laboratory-Based CVD Risk Chart (SEAR-B / Indonesia)" akan menyelaraskan aplikasi secara mutlak dengan Kepmenkes Nomor HK.01.07/MENKES/1186/2022. Studi epidemiologi di wilayah SEAR yang dipublikasikan dalam Health Science Reports (2023; 6(10):e1614; PMID: 37818312; PMCID: PMC10560824; DOI: 10.1002/hsr2.1614) menunjukkan bahwa sementara 80,8% individu berusia 40 hingga 49 tahun masih berada pada strata risiko kurang dari 5% (Rute Hijau), proporsi tersebut turun menjadi 20,4% pada usia 50 hingga 59 tahun dan menjadi 0% pada usia 60 tahun ke atas, di mana mayoritas lansia bergeser ke strata risiko sedang hingga tinggi (10% atau lebih) yang mewajibkan intervensi medis dan pemeriksaan profil lipid/gula darah di FKTP.
Sejalan dengan kalkulasi risiko tersebut, aturan Cross-Validation & Eskalasi (Override Rule) pada Tahap 7 yang secara otomatis membatalkan Rute Hijau dan menaikkan prioritas pasien ke Rute Kuning apabila suhu mencapai 39,5 derajat Celsius atau lebih (hiperpireksia) atau tekanan darah sistolik melebihi 160 mmHg memiliki pijakan klinis yang sangat kokoh. Dalam Pedoman Tatalaksana Hipertensi pada Penyakit Kardiovaskular (PERKI, 2025) dan PNPK Tata Laksana Hipertensi Dewasa (Kepmenkes Nomor HK.01.07/MENKES/4634/2021), tekanan darah sistolik minimal 140 mmHg dan/atau diastolik minimal 90 mmHg merupakan batas penegakan diagnosis hipertensi. Namun, terdapat perbedaan strategi tata laksana yang tajam antara Hipertensi Derajat 1 (sistolik 140 hingga 159 mmHg) dan Hipertensi Derajat 2 (sistolik minimal 160 mmHg atau diastolik minimal 100 mmHg): pada Hipertensi Derajat 1 tanpa faktor risiko kardiovaskular lain, modifikasi pola hidup sehat dapat dijalani sebagai tata laksana awal selama 4 hingga 6 bulan, sedangkan pada Hipertensi Derajat 2 atau lebih (Sistolik minimal 160 mmHg) terapi farmakologis antihipertensi wajib segera diinisiasi oleh dokter di FKTP bersamaan dengan intervensi gaya hidup serta penapisan kerusakan organ target (Hypertension-Mediated Organ Damage / HMOD).

Orkestrasi Rute Rujukan, SPGDT PSC 119, dan Interoperabilitas SATUSEHAT HL7 FHIR R4 (Tahap 8, Tahap 9, & Mediko-Legal)
Validasi Protokol Klinis pada Empat Rute Triase (Tahap 8)
Output triase pada Tahap 8 memisahkan intervensi secara tajam berdasarkan tingkat kegawatan klinis, kompetensi layanan primer (SKDI), dan kebutuhan logistik program nasional Kemenkes RI sebagaimana dirangkum dalam tabel matriks rujukan berikut.
Rute Triase (Tahap 8)
Spektrum Diagnosis AI (Infeksi, NTD, & PTM)
Tindakan Sistem, Logistik Obat & Pemeriksaan Penunjang
Protokol Pertolongan Pertama, Edukasi & Target Waktu Klinis
Landasan Regulasi & Pedoman Medis Resmi
1. Rute Hijau (Perawatan Mandiri / Telemedisin / Apotek)
ISPA Ringan, Diare Akut tanpa dehidrasi, Skabies, Tinea, Varicella Ringan, STH ringan, Risiko PTM Rendah (Skor CVD kurang dari 5%), Mialgia Ringan.
Navigasi GPS ke Apotek untuk obat bebas/bebas terbatas/DOWA (Oralit, Zinc, Paracetamol, Krim Miconazole, Krim Permethrin 5% via Apoteker/resep telemedisin); larangan mutlak rekomendasi antibiotik tanpa resep; integrasi tombol Mobile JKN.
Ventilasi jendela pagi hari & etika batuk (ISPA/TBC); dekontaminasi pakaian/selimut dengan air panas lebih dari 60 derajat Celsius (Skabies); pembatasan garam 1 sdt/hari, gula kurang dari 4 sdm/hari, dan olahraga 150 menit/minggu (30–60 menit/hari minimal 3–5 hari/minggu).
Kepmenkes 1186/2022 (SKDI 4A); Pedoman PERKI (2025) & Kepmenkes 4634/2021; Permenkes No. 3 Tahun 2026.
2. Rute Kuning (FKTP Puskesmas / Klinik Pratama)
Infeksi: DBD fase demam biasa, Malaria tanpa komplikasi, Chikungunya akut, Tifoid, Hepatitis A/B, Amebiasis, Leptospirosis dini, Varicella berat. PTM: DM Tipe 2 Stabil, Hipertensi Derajat 1–2, Artritis Gout, Dislipidemia, Neuropati Diabetik.
Penerbitan QR Code Rujukan FKTP & Antrean Mobile JKN; Pop-up instruksi wajib Puasa 10–12 jam (hanya minum air putih) malam hari sebelum pemeriksaan lab PTM (GDP, GD 2 Jam PP, Profil Lipid, Asam Urat, Ureum/Kreatinin, HbA1c) atau lab Infeksi (Darah Rutin serial, NS1, Apusan Darah, Tubex/Widal, Feses).
Pada Gout Akut: kompres es lokal, larangan memijat sendi bengkak, dan hidrasi air putih lebih dari 2 liter/hari (8–16 gelas/hari saat serangan akut). Pada DBD: hidrasi cairan isotonik/oralit 2–3 liter/hari dan pemantauan warning signs.
PNPK Dengue (Kepmenkes 9845/2020 & 4636/2021); Pedoman DM PERKENI (2024); Pedoman Gout IRA (2020 & 2024, ISBN: 978-979-3730-48-6); PNPK PGK (Kepmenkes 1634/2023).
3. Rute Kuning Khusus (Poli Program Nasional Kemenkes)
Tuberkulosis (TBC Paru/Ekstraparu), Kusta (PB/MB), Frambusia, Filariasis Limfatik, Skistosomiasis, Campak Ringan tanpa komplikasi.
Navigasi eksklusif ke Puskesmas/Faskes penyelenggara Poli DOTS & Eradikasi NTD; Pre-Notification kesiapan Ruang Isolasi Infeksi Airborne (khusus TBC & Campak) serta jaminan stok logistik OAT, Blister MDT Kusta (PB 6 blister / MB 12 blister), Azitromisin POPM Frambusia, dan pot tinja Kato-Katz / Praziquantel.
Edukasi penggunaan masker bedah bagi suspek TBC/Campak sejak dari rumah untuk memutus rantai transmisi droplet/airborne; penapisan kontak serumah untuk kemoprofilaksis Rifampisin dosis tunggal pada Kusta atau POPM Azitromisin pada Frambusia.
Permenkes No. 3 Tahun 2026; Permenkes 11/2019 & Kepmenkes 308/2019 (Kusta); Permenkes 8/2017 (Frambusia); Permenkes 94/2014 (Filariasis).
4. Rute Merah (IGD FKRTL & SPGDT PSC 119)
Infeksi: Syok Dengue (DSS), Malaria Serebral, Gagal Ginjal Leptospirosis, Pneumonia/Campak Berat dengan stridor, Ensefalitis Rabies, TBC Hemoptisis Masif. PTM: STEMI, Stroke Akut, Krisis Hipertensi/Ensefalopati, Koma Diabetik (KAD/SHH/Hipoglikemia Berat).
Aktivasi sirene visual/audio & tombol [ Panggil Ambulans (119) ] terhubung ke NCC/PSC 119; transmisi otomatis Pre-Arrival Tele-triage Data & koordinat GPS ke SIMRS IGD rujukan; Live Tracking ambulans.
Target Waktu Kritis: Door-to-Balloon / EKG kurang dari 10 menit (STEMI); Door-to-Needle kurang dari 30 menit dalam Golden Hour kurang dari 4,5 jam (Trombolisis Stroke); Resusitasi Cairan kurang dari 15 menit (DSS). First Aid: Irigasi luka gigitan rabies dengan sabun & air mengalir 15 menit; status puasa mutlak (NPO) bila kesadaran turun; panduan visual BHD/RJP.
Permenkes No. 19 Tahun 2016 tentang SPGDT (Pasal 5 ayat (3) & Pasal 27 ayat (3) huruf b); Pedoman STEMI & Hipertensi Emergensi PERKI (2025); PNPK Stroke PERDOSSI.

Analisis mendalam terhadap protokol masing-masing rute di atas menunjukkan betapa krusialnya pemisahan jalur rujukan ini dalam ekosistem Jaminan Kesehatan Nasional (JKN). Pada Rute Hijau, larangan mutlak bagi AI untuk merekomendasikan antibiotik atau obat keras tanpa resep dokter menjaga kepatuhan terhadap kebijakan pengendalian resistensi antimikroba nasional (Permenkes Nomor 28 Tahun 2021 dan Permenkes Nomor 3 Tahun 2026). Sebagai catatan tata kelola kefarmasian yang presisi, Krim Permethrin 5% yang tercantum pada Rute Hijau untuk terapi skabies secara regulasi BPOM dan Standar Pelayanan Kefarmasian termasuk golongan obat keras yang dapat diserahkan oleh Apoteker di Apotek melalui skema Daftar Obat Wajib Apotek (DOWA) atau melalui resep elektronik dokter via fitur telemedisin Mobile JKN yang telah diintegrasikan pada antarmuka Rute Hijau. Sementara itu, intervensi gaya hidup pada Rute Hijau—yakni pembatasan asupan garam maksimal 1 sendok teh per hari, gula kurang dari 4 sendok makan per hari, dan olahraga teratur 30 hingga 60 menit per hari minimal 3 hingga 5 hari seminggu (150 menit/minggu)—selaras sepenuhnya dengan rekomendasi non-farmakologis PERKI (2025) dan Kepmenkes Nomor HK.01.07/MENKES/4634/2021.
Pada Rute Kuning, fitur otomatis yang menginstruksikan pasien PTM untuk menjalani puasa 10 hingga 12 jam (hanya diperbolehkan minum air putih) sejak malam hari sebelum mendatangi Puskesmas keesokan paginya merupakan terobosan rekayasa alur klinis yang sangat efektif. Dalam praktik sehari-hari di FKTP, ribuan pasien lansia terpaksa membatalkan pemeriksaan darah dan mengulang antrean di hari lain karena datang dalam kondisi post-prandial (sudah sarapan). Berdasarkan Pedoman Pengelolaan dan Pencegahan DM Tipe 2 Dewasa (PERKENI, 2024) dan Pedoman Dislipidemia PERKI/PERKENI, pemeriksaan Gula Darah Puasa (GDP) mensyaratkan puasa kalori minimal 8 jam, sedangkan pemeriksaan Profil Lipid lengkap mensyaratkan puasa 10 hingga 12 jam guna mencegah elevasi trigliserida serum akibat kilomikron post-prandial yang dapat mendistorsi kalkulasi kolesterol LDL. Pada aspek pertolongan pertama Artritis Gout di Rute Kuning, instruksi kompres es dan larangan keras memijat sendi yang bengkak didukung penuh oleh Pedoman IRA (2020 & 2024), karena manipulasi mekanis atau pemijatan pada sendi yang mengalami inflamasi akut akan memobilisasi pelepasan kristal monosodium urate (MSU) lebih banyak ke dalam cairan sinovial dan memperhebat badai sitokin IL-1, sembari pasien diarahkan ke dokter FKTP untuk mendapatkan terapi lini pertama gout akut onset kurang dari 12 jam (kolkisin dosis rendah 0,5 hingga 1 mg, OAINS, atau kortikosteroid sesuai fungsi ginjal/bersihan kreatinin) serta hidrasi cairan lebih dari 2 liter/hari (minimal 8 hingga 16 gelas/hari saat serangan akut) guna mencegah urolitiasis asam urat.
Pemisahan Rute Kuning Khusus untuk TBC, Kusta, Frambusia, Filariasis, Skistosomiasis, dan Campak menjawab tantangan rantai pasok logistik kesehatan masyarakat Indonesia. Obat-obatan untuk pemberantasan penyakit ini merupakan komoditas program strategis nasional yang dikelola secara terpusat oleh Kemenkes RI dan Dinas Kesehatan Daerah, sehingga tidak tersedia di apotek komersial biasa. Pada penyakit Kusta, Permenkes Nomor 11 Tahun 2019 dan Kepmenkes Nomor HK.01.07/MENKES/308/2019 menetapkan rejimen Multi-Drug Therapy (MDT) gratis di Puskesmas: pasien Kusta Pausibasiler (PB) diberikan MDT PB (berisi dosis bulanan yang diawasi petugas berupa Rifampisin dan Dapson, serta dosis harian hari ke-2 hingga ke-28 berupa Dapson) sebanyak 6 blister yang harus diselesaikan dalam waktu 6 hingga 9 bulan; sedangkan pasien Kusta Multibasiler (MB) diberikan MDT MB (berisi dosis bulanan Rifampisin, Dapson, dan Klofazimin, serta dosis harian Dapson dan Klofazimin) sebanyak 12 blister dalam waktu 12 hingga 18 bulan, disertai pemberian kemoprofilaksis Rifampisin dosis tunggal bagi kontak erat. Untuk Frambusia, Permenkes Nomor 8 Tahun 2017 Pasal 9 hingga Pasal 15 memandatkan bahwa penemuan minimal satu kasus frambusia di suatu desa mengharuskan penyelenggaraan Pemberian Obat Pencegahan Massal (POPM) menggunakan Azitromisin serta surveilans serologis tahunan selama tiga tahun berturut-turut. Untuk Skistosomiasis, rujukan ke Puskesmas di wilayah endemis Sulawesi Tengah memungkinkan pengambilan sampel tinja menggunakan protokol tiga pot tinja selama tiga hari berturut-turut yang diperiksa dengan metode Kato-Katz (menghitung rasio tinja positif telur Schistosoma japonicum) untuk pemberian terapi definitif Praziquantel. Selain aspek obat, pengiriman sinyal Pre-Notification ke Puskesmas agar menyiapkan Ruang Isolasi Airborne sebelum pasien suspek TBC atau Campak tiba sangat krusial untuk mencegah infeksi nosokomial di ruang tunggu FKTP.
Pada Rute Merah, integrasi tombol darurat [ Panggil Ambulans (119)[span_353](start_span)[span_353](end_span)[span_358](start_span)[span_358](end_span) ] dan transmisi otomatis Pre-Arrival Tele-triage Data ke National Command Center (NCC) 119 / Public Safety Center (PSC) 119 serta SIMRS IGD rumah sakit rujukan merupakan implementasi langsung dari Peraturan Menteri Kesehatan Republik Indonesia Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT) yang tercatat dalam basis data resmi JDIH BPK RI dan Direktorat Pelayanan Kesehatan Rujukan Kemenkes RI. Dalam regulasi tersebut, Pasal 5 ayat (3) dan Pasal 27 ayat (3) huruf b mewajibkan setiap Pemerintah Daerah Kabupaten/Kota membentuk dan menyelenggarakan PSC 119 guna mempercepat waktu tanggap (response time) penanganan kegawatdaruratan pra-fasilitas. Pengiriman telemetri pra-fasilitas ini sangat esensial untuk mencapai target waktu kritis: pada krisis hipertensi dengan edema pulmonal akut atau iskemia serebral, Pedoman PERKI (2025) menginstruksikan penurunan Mean Arterial Pressure (MAP) sebesar 25% pada 1 jam pertama secara terkontrol di IGD (menggunakan agen intravena seperti beta-blocker atau nitrogliserin, dengan kehati-hatian agar tekanan diastolik tidak turun di bawah 60 mmHg pada pasien penyakit jantung koroner); sementara pada Syok Dengue (DSS), pemberian resusitasi cairan intravena dini di ruang emergensi terbukti menurunkan risiko kematian hingga di bawah 0,5%. Terkait instruksi pertolongan pertama (First Aid) pada Rute Merah, larangan memberi makan atau minum per oral (Nil Per Os / NPO) saat kesadaran menurun sudah sangat tepat. Namun, pengembang perlu mempertajam instruksi posisi tubuh pasien: pada pasien Stroke Akut dengan penurunan kesadaran, posisi terbaik untuk menjaga patensi jalan napas dan mencegah aspirasi muntahan adalah posisi pemulihan miring (lateral recovery position) sebagaimana tercantum pada panduan BHD aplikasi (sedangkan elevasi kepala 30 derajat dikhususkan bagi pasien dengan peningkatan tekanan intrakranial yang jalan napasnya telah aman); sementara pada Syok Dengue (DSS), peninggian kaki (passive leg raising) hanya boleh dilakukan apabila pasien tidak mengalami sesak napas akibat efusi pleura masif atau edema paru akut.
Standar Interoperabilitas SATUSEHAT HL7 FHIR R4 dan Mobile JKN (Tahap 9)
Peta jalan integrasi pada Tahap 9 memenuhi mandat transformasi teknologi kesehatan nasional berdasarkan Permenkes Nomor 24 Tahun 2022 tentang Rekam Medis (yang mewajibkan seluruh fasyankes menyelenggarakan Rekam Medis Elektronik / RME dengan masa retensi penyimpanan minimal 25 tahun sejak kunjungan terakhir pasien) dan platform interoperabilitas nasional SATUSEHAT yang dibangun di atas standar HL7 FHIR (Fast Healthcare Interoperability Resources) Release 4 (R4) sebagaimana diatur dalam Pedoman Tata Kelola Rumah Sakit Bidang Operasional Kemenkes RI. Agar fitur pemindaian QR Code Handover di Puskesmas dapat langsung menginjeksi data ke dalam SIMRS/SIMPUS tanpa perlu entri ulang oleh dokter atau perawat, struktur data di balik QR Code tersebut wajib memetakan variabel triase ke dalam Resource FHIR R4 dan kamus terminologi klinis baku Kemenkes RI sebagaimana dirinci pada tabel spesifikasi berikut.
Komponen Data pada QR Code Aplikasi
HL7 FHIR R4 Resource Standar SATUSEHAT
Sistem Kode / Terminologi Wajib Kemenkes RI
Implementasi Spesifik pada Blueprint Triase
Identitas & Demografi Pasien (Tahap 1)
Patient & Encounter
NIK (Nomor Induk Kependudukan) / IHS Number SATUSEHAT
Memetakan usia, jenis kelamin administratif (male / female), dan mengaitkan sesi triase mandiri dengan kunjungan fasyankes melalui Resource Encounter.
Tanda Vital, Antropometri, & Skor CVD (Tahap 6 & 7)
Observation (Kategori: vital-signs & exam)
LOINC (Logical Observation Identifiers Names and Codes) & UCUM (Satuan Ukur)
Mengkodekan Suhu tubuh (8310-5 dalam derajat Celsius), Tekanan Darah Sistolik (8480-6), Diastolik (8462-4), Tinggi Badan (8302-2), Berat Badan (29463-7), IMT (39156-5), Lingkar Pinggang (8280-0), serta Status Kehamilan (82810-3).
Keluhan Utama, HPI, & Suspek Diagnosis AI (Tahap 2, 5, 8)
Condition (verificationStatus: provisional / differential)
ICD-10 (untuk diagnosis kerja/klaim JKN) & SNOMED-CT (untuk keluhan klinis)
Mengkodekan suspek penyakit ke ICD-10 (contoh: J06 untuk ISPA akut, A91 untuk DBD, A15 untuk TBC Paru, A30 untuk Kusta, A66 untuk Frambusia, B65.2 untuk Schistosoma japonicum, E11 untuk DM Tipe 2, I10 untuk Hipertensi, M10 untuk Gout).
Riwayat Obat Rutin & Peringatan Interaksi (Tahap 4 - Q5)
M[span_121](start_span)[span_121](end_span)[span_126](start_span)[span_126](end_span)edicationStatement & DetectedIssue (untuk peringatan CDSS)
KFA (Kamus Farmasi dan Alat Kesehatan Kemenkes RI)
Mencatat konsumsi NSAID, Loperamide, Amlodipine, atau Captopril menggunakan kode presisi KFA agar sistem RME apoteker dan dokter di FKTP langsung menerima flag potensi interaksi obat secara otomatis.
Rekomendasi Pemeriksaan Laboratorium (Tahap 8 - Rute Kuning)
ServiceRequest (Kategori: Laboratory procedure)
LOINC & SNOMED-CT
Mengirimkan draf pengantar pesanan lab (Darah Rutin, NS1, GDP, Profil Lipid, Asam Urat, Kreatinin, TCM TBC, Kato-Katz) beserta atribut patientInstruction berisi mandat puasa 10–12 jam.
Pendaftaran Antrean Online & Rujukan (Tahap 8 & 9)
Appointment & ServiceRequest (Rujukan)
API Web Service BPJS Kesehatan (Antrean Online FKTP / Mobile JKN & PCare)
Menghubungkan tombol "Buat Janji / Daftar Poli" ke endpoint antrean FKTP terdaftar milik peserta JKN untuk memangkas hambatan administratif di Puskesmas.

Kepatuhan Mediko-Legal dan Perlindungan Data Pribadi
Rumusan Disclaimer & Penafian Mediko-Legal yang diwajibkan tampil pada layar hasil triase telah memenuhi standar etika kedokteran dan hukum kesehatan dengan menegaskan bahwa luaran aplikasi merupakan alat bantu triase awal berbasis kecerdasan buatan (Clinical Decision Support / Triage Tool) dan bukan diagnosis medis final maupun pengganti pemeriksaan fisik dan laboratorium oleh dokter. Dari perspektif hukum positif Indonesia, penafian ini berinteraksi erat dengan Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan dan Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP). Mengingat studi literatur hukum kesehatan digital di Indonesia menyoroti tingginya kerentanan kebocoran data medis dan penyalahgunaan data oleh pihak ketiga pada platform telemedisin, keputusan arsitektural pada Tahap 7 untuk menjalankan inferensi model secara lokal di dalam perangkat ponsel pengguna (Edge AI on-device processing) memberikan perlindungan Privacy-by-Design yang sangat kuat. Data biometrik dan citra klinis sensitif (seperti foto lesi kusta, frambusia, atau skabies pada Q8) diproses di memori lokal ponsel tanpa harus diunggah ke peladen awan (cloud server) pihak ketiga, sementara pengiriman ringkasan data menuju SATUSEHAT, Mobile JKN, atau PSC 119 hanya dieksekusi berdasarkan persetujuan sah (explicit informed consent) pasien atau dalam kondisi darurat penyelamatan nyawa pada Rute Merah.
Sintesis Rekomendasi Strategis Penyempurnaan Blueprint Aplikasi
Secara keseluruhan, rancangan Blueprint Aplikasi: Triase Adaptif Infeksi Tropis, NTD & PTM telah memiliki kepadatan klinis, akurasi epidemiologis, dan keselarasan regulasi yang sangat tinggi. Sebagai langkah finalisasi sebelum dokumen spesifikasi ini diajukan ke dalam pengujian Regulatory Sandbox Kemenkes RI atau uji validasi klinis prospektif di FKTP, terdapat lima rekomendasi penyempurnaan presisi yang disarikan dalam tabel matriks tindakan berikut.
Tahap Blueprint
Komponen Saat Ini
Rekomendasi Penyempurnaan Presisi
Rujukan Resmi Utama (Regulasi / WHO / DOI Jurnal)
Tahap 3 & Tahap 8 (Red Flags & First Aid)
Deskripsi kualitatif oliguria (6–8 jam) dan instruksi posisi baring kaki ditinggikan pada Syok / kepala 30 derajat pada Stroke.
Menambahkan parameter kuantitatif internal oliguria (kurang dari 0,5 mL/kg/jam dewasa atau kurang dari 1,5 mL/kg/jam dengue) dan CRT lebih dari 2 detik. Memisahkan instruksi posisi: gunakan posisi pemulihan miring (lateral recovery position) pada pasien stroke/penurunan kesadaran untuk cegah aspirasi, dan batasi peninggian kaki pada Syok Dengue hanya bila tidak ada sesak napas (edema paru/efusi pleura).
PNPK Infeksi Dengue (Kepmenkes 9845/2020 & 4636/2021); PMCID: PMC11239217 (DOI: 10.61622/rbgo/2024rbgo73); PMCID: PMC11233874.
Tahap 4 (Q5 - Trigger AI Obat)
Empat Trigger AI (DBD + NSAID; Diare + Antimotilitas; Amlodipine vs. Filariasis; Captopril vs. TBC).
Menambahkan Sub-Trigger AI 1B (Komorbid PTM pada Suspek DBD): Peringatan evaluasi penghentian sementara Statin (risiko cedera hepar/transaminase), Diuretik/Antihipertensi (risiko memperberat syok saat plasma leakage), dan Antikoagulan/Warfarin (risiko perdarahan GI masif).
PMCID: PMC11233874; NCBI Bookshelf NBK542299; PMCID: PMC8389296; DOI: 10.1038/s41598-022-18654-2.
Tahap 5 & Tahap 6 (Deteksi Kusta)
Anamnesis bercak mati rasa (Klaster 4) dan Computer Vision bercak putih mati rasa (Q8).
Menerapkan aturan Rule-Based Multimodal Override: karena sensitivitas Computer Vision aplikasi WHO Skin NTDs turun menjadi 69,6% pada kusta reaksional/atipikal (dibandingkan 87,2% pada kusta klasik), hasil uji mandiri mati rasa tusuk jarum atau nyeri/penebalan saraf tepi wajib otomatis mengunci Rute Kuning Khusus meskipun confidence score visual kamera rendah.
Permenkes 11/2019 & Kepmenkes 308/2019; PMCID: PMC13086047; Yotsu et al., PLOS Negl Trop Dis 2023 (DOI: 10.1371/journal.pntd.0011230).
Tahap 7 (Skor Risiko Kardiovaskular)
CVD Risk Score (Framingham Adaptasi) menggunakan Usia, Lingkar Perut, BMI, dan Merokok.
Mengubah nomenklatur dan rumus menjadi WHO Non-Laboratory-Based Cardiovascular Disease Risk Chart (SEAR-B / Indonesia) berbasis 5 variabel (Usia 40–74 tahun, Jenis Kelamin, Status Merokok, Tekanan Darah Sistolik, dan IMT) dengan pita risiko kurang dari 5%, 5% hingga kurang dari 10%, 10% hingga kurang dari 20%, 20% hingga kurang dari 30%, dan 30% atau lebih.
Pedoman Puskesmas Klaster 3 Kemenkes RI; Kepmenkes 1186/2022; Konsensus InaSH; DOI: 10.1002/hsr2.1614; DOI: 10.1016/S2213-8587(23)00119-5.
Tahap 8 & Tahap 9 (Regulasi & SATUSEHAT)
Rekomendasi Krim Permethrin 5% di Rute Hijau & QR Code Handover RME Puskesmas.
Mencantumkan status penyerahan Krim Permethrin 5% melalui Apoteker (DOWA) atau e-resep telemedisin JKN; menyelaraskan referensi regulasi ke Permenkes Nomor 3 Tahun 2026; serta menstandardisasi skema JSON QR Code ke dalam Resource HL7 FHIR R4 SATUSEHAT dengan pengkodean LOINC, ICD-10, SNOMED-CT, dan KFA.
UU Kesehatan No. 17 Tahun 2023; Permenkes No. 3 Tahun 2026; Permenkes No. 24 Tahun 2022; Pedoman RS Kemenkes 2025.



1. Ahmed, S., et al. (2024). Case report: Escitalopram-associated lower limb edema and differential diagnosis of drug-associated lower limb edema (PMID: 38736624; PMCID: PMC11082315). Frontiers in Psychiatry, 15, 1394813. https://doi.org/10.3389/fpsyt.2024.1394813 (Tautan web: https://pmc.ncbi.nlm.nih.gov/articles/PMC11082315/)
2. Alam, S. M., Qasswal, M., Ahsan, M. J., Walters, R. W., & Chandra, S. (2022). Selective serotonin reuptake inhibitors increase risk of upper gastrointestinal bleeding when used with NSAIDs: A systemic review and meta-analysis. Scientific Reports, 12(1), 14452. https://doi.org/10.1038/s41598-022-18654-2
3. American Academy of Family Physicians. (2022). Acute diarrhea in adults: Evaluation and management clinical guideline. American Family Physician, 106(1), 72–80. https://www.aafp.org/afp/2022/0700/acute-diarrhea
4. Barrera, R., et al. (2023). Dengue, chikungunya and Zika arbovirus infections in Caribbean and tropical regions (PMCID: PMC10090388). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC10090388/
5. Chansrichavala, P., et al. (2015). Loperamide therapy for voluminous diarrhea in infectious disease settings (PMCID: PMC4366607). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC4366607/
6. Deps, P., Amorim, B. B. C., Repsold, T., & Almonfrey, D. (2025a). Independent assessment of the World Health Organization Skin Neglected Tropical Diseases application for leprosy detection (Avaliação independente do aplicativo Skin Neglected Tropical Diseases da OMS para detecção da hanseníase) (PMID: 42006576; PMCID: PMC13086047). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC13086047/
7. Deps, P., et al. (2025b). Artificial intelligence and integrated management of skin-related neglected tropical diseases. British Journal of Dermatology, 193(Suppl. 1), ljaf212. https://doi.org/10.1093/bjd/ljaf212
8. Dicpinigaitis, P. V. (2014). ACE inhibitors: Upper respiratory symptoms, bradykinin accumulation, and differential diagnosis (PMID: 25035451; PMCID: PMC4112303). BMJ Case Reports, 2014, bcr2014205462. https://doi.org/10.1136/bcr-2014-205462 (Tautan web: https://pmc.ncbi.nlm.nih.gov/articles/PMC4112303/)
9. Dinas Kesehatan Provinsi Sulawesi Tengah & Kementerian Kesehatan Republik Indonesia. (2024). Schistosomiasis di Sulawesi Tengah: Epidemiologi, penularan, dan intervensi 2019–2024. Dinas Kesehatan Provinsi Sulawesi Tengah. https://dinkes.sultengprov.go.id/schistosomiasis-di-sulawesi-tengah-epidemiologi-penularan-dan-intervensi-2019-2024/
10. Federação Brasileira das Associações de Ginecologia e Obstetrícia. (2024). Prevention, diagnosis, and treatment protocol of dengue during pregnancy and the postpartum period (PMID: 38994458; PMCID: PMC11239217). Revista Brasileira de Ginecologia e Obstetrícia, 46, e-rbgo73. https://doi.org/10.61622/rbgo/2024rbgo73 (Tautan web: https://pubmed.ncbi.nlm.nih.gov/38994458/)
11. Grobusch, M. P., et al. (2025). Racecadotril versus loperamide for acute diarrhea of infectious origin (PMCID: PMC12098968). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC12098968/
12. Gujarathi, A. P., Powar, J., Patil, R., Padhyegurjar, S., Ghodake, A. K., & Shaikh, M. H. M. A. (2025). Estimation of cardiovascular risk by using WHO/ISH charts and Correlation & Regression Tree (CART) analysis in adults of rural North Maharashtra, India. National Journal of Community Medicine, 16(11), 1101–1108. https://doi.org/10.55489/njcm.161120255801 (Tautan web: https://www.researchgate.net/publication/397166899_Estimation_of_Cardiovascular_Risk_by_Using_WHOISH_charts_and_Correlation_Regression_Tree_CART_Analysis_in_Adults_of_Rural_North_Maharashtra_India)
13. Hengge, U. R., Currie, B. J., Jäger, G., Lupi, O., & Schwartz, R. A. (2007). Scabies: A ubiquitous neglected skin disease. Trends in Parasitology, 23(10), 485–493. https://doi.org/10.1016/j.pt.2007.08.007
14. Herman, L., et al. (2021). Assessment of knowledge, attitudes, and practices regarding dengue and NSAID contraindications among healthcare practitioners (PMCID: PMC8389296). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC8389296/
15. Ikatan Dokter Anak Indonesia. (2022). Pedoman nasional pelayanan kedokteran & konsensus tata laksana infeksi dengue anak dan remaja. Badan Penerbit Ikatan Dokter Anak Indonesia. https://www.idai.or.id/professional-resources/pedoman-konsensus/pedoman-nasional-pelayanan-kedokteran-tata-laksana-infeksi-dengue-anak-dan-remaja
16. Jones, O. T., Matin, R. N., van der Schaar, M., Prathivadi Bhayankaram, K., Ranmuthu, C. K. I., Islam, M. S., Behiyat, D., Boscott, R., Calanzani, N., Emery, J., Williams, H. C., & Walter, F. M. (2022). Artificial intelligence and machine learning algorithms for early detection of skin cancer in community and primary care settings: A systematic review. The Lancet Digital Health, 4(6), e466–e476. https://doi.org/10.1016/S2589-7500(22)00023-1
17. Kamath, S., et al. (2024). Using artificial intelligence on dermatology conditions in Uganda: Epidemiology and burden of tropical skin diseases (PMCID: PMC10782289). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC10782289/
18. Kementerian Kesehatan Republik Indonesia. (2014). Peraturan Menteri Kesehatan Republik Indonesia Nomor 94 Tahun 2014 tentang Penanggulangan Filariasis (Berita Negara Republik Indonesia Tahun 2014 Nomor 2036). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74
19. Kementerian Kesehatan Republik Indonesia. (2016). Peraturan Menteri Kesehatan Republik Indonesia Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT). Direktorat Pelayanan Kesehatan Rujukan Kementerian Kesehatan Republik Indonesia. https://keslan.kemkes.go.id/lakip_files/direktorat_pelayanan_kesehatan_rujukan_rak_2021.pdf
20. Kementerian Kesehatan Republik Indonesia. (2017a). Peraturan Menteri Kesehatan Republik Indonesia Nomor 8 Tahun 2017 tentang Eradikasi Frambusia (Berita Negara Republik Indonesia Tahun 2017 Nomor 351). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/111971/permenkes-no-8-tahun-2017
21. Kementerian Kesehatan Republik Indonesia. (2017b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 15 Tahun 2017 tentang Penanggulangan Cacingan (Berita Negara Republik Indonesia Tahun 2017 Nomor 438). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74
22. Kementerian Kesehatan Republik Indonesia. (2019a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/308/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tatalaksana Kusta. Kementerian Kesehatan Republik Indonesia. https://ayosehat.kemkes.go.id/topik-penyakit/pencegahan-infeksi-pada-usia-produktif/kusta
23. Kementerian Kesehatan Republik Indonesia. (2019b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 11 Tahun 2019 tentang Penanggulangan Kusta (Berita Negara Republik Indonesia Tahun 2019 Nomor 449). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/138606/permenkes-no-11-tahun-2019
24. Kementerian Kesehatan Republik Indonesia. (2020a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/603/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Diabetes Melitus Tipe 2 Dewasa. Kementerian Kesehatan Republik Indonesia. https://rsudhaulussymaluku.com/unduh/4
25. Kementerian Kesehatan Republik Indonesia. (2020b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/9845/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue pada Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.kemkes.go.id/eng/pnpk-2020---tata-laksana-infeksi-dengue-pada-dewasa
26. Kementerian Kesehatan Republik Indonesia. (2021a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4634/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Hipertensi Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.prescribingcompanion.com/indonesia/kondisi-klinis-umum-lainnya/f-kardiovaskular/6-hipertensi-esensial/
27. Kementerian Kesehatan Republik Indonesia. (2021b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4636/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue Anak dan Remaja. Kementerian Kesehatan Republik Indonesia. http://www.kemkes.go.id/id/pnpk-2021---infeksi-dengue-anak-dan-remaja
28. Kementerian Kesehatan Republik Indonesia. (2021c). Peraturan Menteri Kesehatan Republik Indonesia Nomor 28 Tahun 2021 tentang Pedoman Penggunaan Antibiotik (Berita Negara Republik Indonesia Tahun 2021 Nomor 1076). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74
29. Kementerian Kesehatan Republik Indonesia. (2022a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1186/2022 tentang Panduan Praktik Klinis bagi Dokter di Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP). Kementerian Kesehatan Republik Indonesia. https://manuver.tireg7.net/wp-content/uploads/2025/01/KEPMENKES-HK-01-07-MENKES-1186-2022-2.pdf
30. Kementerian Kesehatan Republik Indonesia. (2022b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis (Berita Negara Republik Indonesia Tahun 2022 Nomor 829). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74&tahun=2025
31. Kementerian Kesehatan Republik Indonesia. (2023a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1634/2023 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Penyakit Ginjal Kronik. Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74&tahun=2025
32. Kementerian Kesehatan Republik Indonesia. (2023b). Petunjuk teknis kolaborasi TBC-HIV. Direktorat Jenderal Pencegahan dan Pengendalian Penyakit Kementerian Kesehatan Republik Indonesia. https://kemkes.go.id/
33. Kementerian Kesehatan Republik Indonesia. (2024). Pedoman kerja Puskesmas klaster 3: Kesehatan usia dewasa dan lanjut usia (Memuat statistik Survei Kesehatan Indonesia / SKI 2023 dan tabel prediksi risiko PTM adaptasi WHO Cardiovascular Disease Risk Charts). Kementerian Kesehatan Republik Indonesia. https://renbut.kemkes.go.id/regulasi/Pedoman%20Puskesmas%20Klaster%203.pdf
34. Kementerian Kesehatan Republik Indonesia & Dinas Kesehatan Provinsi Kalimantan Tengah. (2025). Pedoman tata kelola rumah sakit: Buku 4 bidang operasional (Standar interoperabilitas SATUSEHAT HL7 FHIR R4 dan pengkodean LOINC). Kementerian Kesehatan Republik Indonesia. https://dinkes.kalteng.go.id/wp-content/uploads/2025/10/Pedoman-Tata-Kelola-Rumah-Sakit-Buku-4-Bidang-Operasional.pdf
35. Kementerian Kesehatan Republik Indonesia. (2026). Peraturan Menteri Kesehatan Republik Indonesia Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit (Berita Negara Republik Indonesia Tahun 2026 Nomor 173). Biro Hukum Kementerian Kesehatan Republik Indonesia. https://peraturan.go.id/files/permenkes-no-3-tahun-2026.pdf
36. Khanal, P., et al. (2023). Estimation of 10-year cardiovascular risk among adult population in western Nepal using nonlaboratory-based WHO/ISH chart, 2023: A cross-sectional study (PMID: 37818312; PMCID: PMC10560824). Health Science Reports, 6(10), e1614. https://doi.org/10.1002/hsr2.1614 (Tautan web: https://pmc.ncbi.nlm.nih.gov/articles/PMC10560824/)
37. Koo, H. L., DuPont, H. L., & Musher, D. M. (2007). Fulminant amoebic colitis following loperamide use (PMID: 17241255). Journal of Travel Medicine, 14(1), 61–62. https://doi.org/10.1111/j.1708-8305.2006.00095.x (Tautan web: https://pubmed.ncbi.nlm.nih.gov/17241255/)
38. Largeau, B., Cracowski, J. L., Lengellé, C., Sautenet, B., & Jonville-Béra, A. P. (2021). Drug-induced peripheral oedema: An aetiology-based review. British Journal of Clinical Pharmacology, 87(8), 3043–3055. https://doi.org/10.1111/bcp.14752
39. Liang, L., Kung, J. Y., Mitchelmore, B., Cave, A., & Banh, H. L. (2022). Comparative peripheral edema for dihydropyridines calcium channel blockers treatment: A systematic review and network meta-analysis. The Journal of Clinical Hypertension, 24(5), 536–554. https://doi.org/10.1111/jch.14436
40. Makani, H., Bangalore, S., Romero, J., Htyte, N., Berrios, R. S., Makwana, H., & Messerli, F. H. (2011). Peripheral edema associated with calcium channel blockers: Incidence and withdrawal rate—a meta-analysis of randomized trials. Journal of Hypertension, 29(7), 1270–1280. https://doi.org/10.1097/HJH.0b013e3283472643
41. Moffatt, C. J., Franks, P. J., Doherty, D. C., Williams, A. F., Badger, C., Jeffs, E., Bosanquet, N., & Mortimer, P. S. (2003). Lymphoedema: An underestimated health problem. QJM: An International Journal of Medicine, 96(10), 731–738. https://doi.org/10.1093/qjmed/hcg126
42. Mohiuddin, A. K. (2023). Erroneous uses of NSAIDs in patients with COVID-19, dengue, and chikungunya. Universal Journal of Pharmacy and Pharmacology, 2(1), 1–2. https://doi.org/10.31586/ujpp.2023.551 (Tautan web: https://www.scipublications.com/journal/ujpp/article/erroneous-uses-of-nsaids-in-patients-with-covid-19-dengue-and-chikungunya-551)
43. Outlaw, F., Meek, J., MacDonald, L. W., & Leung, T. S. (2020). Smartphone screening for neonatal jaundice via ambient-subtracted scleral chromaticity (PMCID: PMC7051077). PLOS One, 15(3), e0216970. https://pmc.ncbi.nlm.nih.gov/articles/PMC7051077/
44. Paz-Bailey, G., Adams, L. E., Deen, J., Anderson, K. B., & Katzelnick, L. C. (2024). Dengue. JAMA, 331(10), 874–884. https://doi.org/10.1001/jama.2023.27724
45. Pemerintah Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196). Sekretariat Negara Republik Indonesia. https://peraturan.bpk.go.id/Search?entitas=74
46. Pemerintah Republik Indonesia. (2023). Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan (Lembaran Negara Republik Indonesia Tahun 2023 Nomor 105). Sekretariat Negara Republik Indonesia. https://gudangilmu.farmasetika.com/bab-ii-transformasi-teknologi-kesehatan-blueprint/
47. Perhimpunan Dokter Hipertensi Indonesia. (2019). Konsensus penatalaksanaan hipertensi di Indonesia (Tabel prediksi risiko PTM diadaptasi dari WHO Cardiovascular Disease Risk Charts). Perhimpunan Dokter Hipertensi Indonesia (InaSH). https://www.inash.or.id/
48. Perhimpunan Dokter Spesialis Kardiovaskular Indonesia. (2025). Pedoman tatalaksana hipertensi pada penyakit kardiovaskular & sindrom koroner akut. Pengurus Pusat Perhimpunan Dokter Spesialis Kardiovaskular Indonesia (PERKI). https://www.inaheart.org/wp-content/uploads/2025/10/Pedoman-Tatalaksana-Hipertensi-Pada-Penyakit-Kardiovaskular.pdf
49. Perhimpunan Reumatologi Indonesia. (2024). Pedoman diagnosis dan tatalaksana hiperurisemia & artritis gout (Edisi pembaruan; ISBN: 978-979-3730-48-6). Pengurus Besar Perhimpunan Reumatologi Indonesia (IRA). https://reumatologi.or.id/wp-content/uploads/2024/09/ISBN-Hiperurisemia-Artritis-Gout_download.pdf
50. Perkumpulan Endokrinologi Indonesia. (2021). Pedoman petunjuk praktis terapi insulin pada pasien diabetes melitus tahun 2021. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://papdisolo.com/library
51. Perkumpulan Endokrinologi Indonesia. (2024). Pedoman pengelolaan dan pencegahan diabetes melitus tipe 2 dewasa di Indonesia tahun 2024. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://pbperkeni.or.id/wp-content/uploads/2025/08/DMT2-2024-Protected.pdf
52. Putri, R. A., et al. (2025). Pengaruh penggunaan amlodipine terhadap risiko edema perifer pada pasien hipertensi. Jurnal Sains dan Kesehatan, 7(3), 213–221. https://doi.org/10.25026/jsk.v7i3.2460 (Tautan web: https://ejournal.urindo.ac.id/index.php/kesehatan/article/view/7571)
53. Rezaei, F., Seif, M., Fattahi, M. R., Gandomkar, A., & Hasanzadeh, J. (2023). Comparison of laboratory-based and non-laboratory-based WHO cardiovascular disease risk charts: A population-based study (PMID: 37301218). The Lancet Diabetes & Endocrinology, 11(7), 480–490. https://doi.org/10.1016/S2213-8587(23)00119-5
54. Satrija, F., Ridwan, Y., Jastal, Samarang, & Rauf, A. (2017). Current status of schistosomiasis in Indonesia: Epidemiology, transmission, and integrated control. Infectious Diseases of Poverty, 6(1), 1–14. https://doi.org/10.1186/s40249-017-0256-8
55. Savage, R. D., Visentin, J. D., Bronskill, S. E., Wang, X., Gruneir, A., Giannakeas, V., Guan, J., Lam, K., Luke, M. J., Read, S. H., Stall, N. M., Wu, W., Zhu, L., Rochon, P. A., & McCarthy, L. M. (2020). Evaluation of a common prescribing cascade of calcium channel blockers and diuretics in older adults with hypertension. JAMA Internal Medicine, 180(5), 643–651. https://doi.org/10.1001/jamainternmed.2019.7087
56. Schiller, L. R., et al. (2020). Severe acute diarrhea: Pathophysiology, antimotility contraindications, and management (PMCID: PMC7127018). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC7127018/
57. Sharp, T. M., Keating, M. K., Shieh, W. J., Bhatnagar, J., Bollweg, B. C., Levine, R., Blau, D. M., Torres, J. V., Rivera, A., Perez-Padilla, J., Munoz-Jordan, J., Sanabria, D., Fischer, M., & Zaki, S. R. (2021). Clinical characteristics, histopathology, and tissue immunolocalization of chikungunya and dengue virus infections. Clinical Infectious Diseases, 73(2), e345–e354. https://doi.org/10.1093/cid/ciaa837
58. Sica, D. A. (2003). Calcium channel blocker-related peripheral edema: Can it be resolved? The Journal of Clinical Hypertension, 5(4), 291–295. https://doi.org/10.1111/j.1524-6175.2003.02402.x (Tautan web: https://www.researchgate.net/publication/10596282_Calcium_Channel_Blocker-Related_Peripheral_Edema_Can_It_Be_Resolved)
59. Tovar, J. H., Pinzón, M. A., Rincón, D. F., et al. (2024). Anesthesia and perioperative care management in patients with dengue fever: Coagulopathy, plasma leakage, and comorbid medications (PMID: 38723714; PMCID: PMC11233874). Brazilian Journal of Anesthesiology, 74(4), 844521. https://pmc.ncbi.nlm.nih.gov/articles/PMC11233874/ (Beserta laporan kasus perdarahan saluran cerna dengue: https://doi.org/10.1016/j.ijscr.2013.08.017)
60. U.S. National Library of Medicine, National Institutes of Health. (2024a). Angiotensin-converting enzyme inhibitors (ACEI) (StatPearls Bookshelf ID: NBK431051). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK431051/
61. U.S. National Library of Medicine, National Institutes of Health. (2024b). DailyMed official drug monograph: Loperamide hydrochloride capsule (SetID: 1be585e2-ef49-4210-8a2d-22a326e4cc1b). National Institutes of Health. https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1be585e2-ef49-4210-8a2d-22a326e4cc1b
62. U.S. National Library of Medicine, National Institutes of Health. (2024c). Ibuprofen (StatPearls Bookshelf ID: NBK542299). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK542299/
63. U.S. National Library of Medicine, National Institutes of Health. (2024d). Loperamide (StatPearls Bookshelf ID: NBK557885). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK557885/
64. Wang, L., et al. (2021). Neonatal jaundice detection using a computer vision system. Designs, 5(4), 63. https://doi.org/10.3390/designs5040063 (Tautan web: https://www.mdpi.com/2411-9660/5/4/63)
65. Wang, Y., et al. (2023). Non-invasive and non-contact automatic jaundice detection of neonates and adults using computer vision. Computer Methods in Biomechanics and Biomedical Engineering: Imaging & Visualization, 11(6), 2244601. https://doi.org/10.1080/21681163.2023.2244601 (Tautan web: https://www.tandfonline.com/doi/full/10.1080/21681163.2023.2244601)
66. Widjaja, J., Anastasia, H., Nurwidayati, A., Nurjana, M. A., Mujiyanto, & Maksud, M. (2017). Situasi terkini daerah fokus keong hospes perantara di daerah endemis schistosomiasis di Sulawesi Tengah. Buletin Penelitian Kesehatan, 45(4), 215–222. https://doi.org/10.22435/bpk.v45i4.7570.215-222 (Tautan web: https://www.badankebijakan.kemkes.go.id/repositori/id/eprint/5684/1/222771-situasi-terkini-daerah-fokus-keong-hospe-c4559a11-215-222.pdf)
67. World Health Organization. (2009). Dengue: Guidelines for diagnosis, treatment, prevention and control (New ed.). World Health Organization. https://www.who.int/publications/i/item/9789241547871
68. World Health Organization, Regional Office for South-East Asia. (2011). Comprehensive guidelines for prevention and control of dengue and dengue haemorrhagic fever (Revised and expanded ed.). World Health Organization. https://iris.who.int/handle/10665/204894
69. World Health Organization. (2022). Ending the neglect to attain the Sustainable Development Goals: A strategic framework for integrated control and management of skin-related neglected tropical diseases. World Health Organization. https://www.who.int/publications/i/item/9789240051423
70. World Health Organization Indonesia. (2023, 25 Juli). Overcoming challenges to eliminate schistosomiasis in Central Sulawesi (Mengatasi tantangan untuk mengeliminasi schistosomiasis di Sulawesi Tengah). World Health Organization. https://www.who.int/indonesia/id/news/detail/25-07-2023-overcoming-challenges-to-eliminate-schistosomiasis-in-central-sulawesi
71. Yotsu, R. R., Ding, Z., Hamm, J., & Blanton, R. E. (2023a). Deep learning for AI-based diagnosis of skin-related neglected tropical diseases: A pilot study (PMID: 37578966; PMCID: PMC10449179). PLOS Neglected Tropical Diseases, 17(8), e0011230. https://doi.org/10.1371/journal.pntd.0011230 (Preprint medRxiv: https://doi.org/10.1101/2023.03.14.23287243; Tautan web: https://pmc.ncbi.nlm.nih.gov/articles/PMC10449179/)
72. Yotsu, R. R., et al. (2023b). Integrated control and management of skin-related neglected tropical diseases. PLOS Neglected Tropical Diseases, 17(6), e0011357. https://doi.org/10.1371/journal.pntd.0011357
73. Yotsu, R. R., Oiwoh, S. O., Mbali, H., Parajuli, N., Enbiale, W., & Ruiz-Postigo, J. A. (2025). Harnessing artificial intelligence for skin-related neglected tropical diseases (skin NTDs): Opportunities, challenges and future directions (PMID: 40590239; PMCID: PMC12406799). International Health, 17(5), 792–794. https://doi.org/10.1093/inthealth/ihaf068 (Tautan web: https://pubmed.ncbi.nlm.nih.gov/40590239/)
74. Zhang, H., et al. (2024). Robust visual identification of under-resourced dermatological conditions: Background pixel separation on the Fitzpatrick 17k dataset in lower and middle income countries (PMCID: PMC12099365). National Center for Biotechnology Information (NCBI). https://pmc.ncbi.nlm.nih.gov/articles/PMC12099365/
75. Zheng, X., et al. (2026). Incidence and risk factors of calcium channel blocker-related edema in hypertensive patients: A multicenter retrospective cohort study. PLOS One, 21(3), e0336659. https://doi.org/10.1371/journal.pone.0336659 (Tautan web: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0336659)
COVER








































DAFTAR ISI

BAB I PENDAHULUAN	4
1.1 Latar Belakang dan Validasi Masalah	4
1.2 Rumusan Masalah	5
1.3 Tujuan Inovasi	6
1.4 Landasan Regulasi dan Kepatuhan Hukum Nasional	6
BAB II KONSEP SOLUSI & KEUNGGULAN EKOSISTEM WEB SIKLUS TERTUTUP	8
2.1 Gambaran Umum Arsitektur Klinis 4 Lapisan (9 Tahap)	8
2.2 Keunggulan Strategis Platform Berbasis Web (Web-First Clinical Ecosystem)	8
2.3 Matriks Keunggulan Kompetitif (Unique Value Proposition)	9
BAB III PROTOKOL KLINIS, PEMETAAN SPASIO-EKOLOGIS & ALGORITMA MEDIS (TAHAP 1-6)	11
3.1 Filter Demografi Absolut (Tahap 1), Keluhan Utama (Tahap 2), dan Primary Survey 11 Red Flags (Tahap 3)	11
3.2 Pemetaan Ekologi One Health (Tahap 4 - Q4) dan Sistem Pakar Farmakovigilans Obat (Tahap 4 - Q5)	14
3.3 Protokol Anamnesis Mendalam Dinamis (Tahap 5) pada 32 Entitas Penyakit	15
3.4 Objektivikasi Klinis Mandiri, Kalibrasi Fitzpatrick IV-VI & Skor Risiko CVD WHO SEAR-B (Tahap 6-7)	19
BAB IV ARSITEKTUR SISTEM WEB, PEMODELAN KECERDASAN BUATAN & REKAYASA PERANGKAT LUNAK (TAHAP 7)	21
4.1 Arsitektur Ekosistem Web Progresif (PWA), Dual-Sided Web Dashboard, dan Tech Stack Keseluruhan	21
4.2 Pemodelan Machine Learning untuk Imputasi Proksi Antropometri dan Klasifikasi Gejala Tabular	21
4.3 Arsitektur Computer Vision Terkalibrasi Fitzpatrick IV-VI, Segmentasi Piksel Latar Belakang, dan Kromatisitas Sklera Digital	21
4.4 Rekayasa Rule Engine Deterministik, Multimodal Override, dan Inferensi Lokal di Peramban (In-Browser Client-Side Inference)	21
4.5 Keamanan Siber Web, Enkripsi Data Lokal (Privacy-by-Design), dan Pengujian Performa Sistem	21
BAB V ORKESTRASI RUJUKAN BERJENJANG, SPGDT PSC 119 & INTEROPERABILITAS SATUSEHAT HL7 FHIR R4 (TAHAP 8-9)	22
5.1 Protokol Klinis dan Logistik pada Empat Rute Triase Berjenjang (Tahap 8)	22
5.2 Prosedur Aktivasi Darurat SPGDT PSC 119 dan Protokol Pertolongan Pertama (First Aid) Presisi	25
5.3 Standar Interoperabilitas RME SATUSEHAT HL7 FHIR R4 dan Mobile JKN (Tahap 9)	26
5.4 Kepatuhan Mediko-Legal dan Perlindungan Data Pribadi	28
BAB VI DAMPAK SISTEMIK, KEBERLANJUTAN & PETA JALAN IMPLEMENTASI	29
6.1 Matriks Dampak Terukur (Key Performance Indicators) terhadap Subtema Healthcare	29
6.2 Strategi Implementasi Ekosistem Nasional & Keberlanjutan (Sustainability)	30
6.3 Peta Jalan Pengembangan (Development Roadmap)	31
DAFTAR PUSTAKA	32



































BAB I PENDAHULUAN

1.1 Latar Belakang dan Validasi Masalah
Transformasi layanan kesehatan primer di Indonesia masih menghadapi empat hambatan struktural dari tingkat rumah tangga hingga Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP):
Penumpukan antrian, Administrasi Manual, dan Pengelolaan Data yang Belum Optimal di Puskesmas/Klinik:
Puskesmas dan klinik kewalahan menghadapi antrian yang panjang, administrasi manual, serta pengelolaan data pasien yang belum optimal. Secara operasional dan klinis, masalah ini dipicu oleh tiga faktor: (a) masuknya kasus ringan tanpa komplikasi (Tingkat Kemampuan 4A pada Standar Kompetensi Dokter Indonesia / SKDI) yang seharusnya tuntas melalui perawatan mandiri di rumah (Kemenkes RI, 2022a); (b) batalnya pemeriksaan laboratorium ribuan pasien PTM/lansia di Puskesmas karena datang dalam kondisi sudah sarapan (post-prandial), padahal pemeriksaan Gula Darah Puasa (GDP) dan Profil Lipid mewajibkan puasa 8 hingga 12 jam (Perkumpulan Endokrinologi Indonesia [PERKENI], 2024); serta (c) beban pencatatan anamnesis berulang secara manual oleh tenaga medis ke dalam sistem Rekam Medis Elektronik (RME).
Kendala Jarak, Biaya Transportasi, dan Bias Deteksi di Wilayah Kepulauan serta Pedalaman:
Masyarakat di wilayah kepulauan dan pedalaman terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan. Di wilayah berkembang, rasio dokter terhadap pasien dapat mencapai 1:25.000 dengan kelangkaan ekstrem dokter spesialis dermatologi, padahal penyakit kulit menempati urutan keempat penyebab disabilitas non-fatal global (Years Lived with Disability) (Kamath et al., 2024). Ketika warga di daerah endemis (seperti Papua, Maluku, NTT, atau 28 desa endemis Skistosomiasis di Sulawesi Tengah) mengalami demam tropis atau lesi kulit NTD, kesalahan mengunjungi fasilitas yang tidak memiliki stok obat program nasional (MDT Kusta, OAT, Azitromisin POPM, atau Praziquantel) menyebabkan pemborosan biaya transportasi yang berat. Di sisi lain, algoritma kecerdasan buatan dermatologi konvensional yang dilatih pada kulit terang (Fitzpatrick I-III) mengalami penurunan kinerja tajam saat diterapkan pada populasi tropis berkulit sawo matang hingga gelap (Fitzpatrick IV-VI) (Jones et al., 2022).
Rendahnya Pemeriksaan Rutin dan Kebutuhan Pemantauan Dini pada Usia Produktif:
Usia produktif yang berisiko diabetes, hipertensi, atau penyakit kronis lain jarang memeriksakan diri, sehingga membutuhkan cara pemantauan dini yang lebih mudah dijangkau. Laporan Survei Kesehatan Indonesia (SKI) 2023 membuktikan bahwa secara nasional 80,82% penduduk dewasa tidak pernah mengukur lingkar perut, 62,6% tidak pernah memeriksa kadar gula darah, 61,6% tidak pernah memeriksa kolesterol, dan 35,61% tidak memantau berat badan, sementara prevalensi hipertensi dan diabetes meningkat signifikan mulai usia 40 tahun ke atas (p<0,01) dan prevalensi TBC usia produktif (25-34 tahun) mencapai 0,42% (Kemenkes RI, 2024; Khanal et al., 2023).
Kesulitan Pemantauan Lansia, Risiko Obat Mandiri, dan Keterlambatan Akses Bantuan Darurat:
Keluarga yang merawat lansia kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, dan menjangkau bantuan sehari-hari, sehingga kondisi lansia berisiko memburuk tanpa terdeteksi. Di masyarakat, swamedikasi obat anti-nyeri NSAID (Ibuprofen/Aspirin) pada demam dengue memicu perdarahan saluran cerna masif (Alam et al., 2022; Mohiuddin, 2023), sedangkan penggunaan antimotilitas (Loperamide) pada disentri memicu kolitis fulminan dan toxic megacolon (Koo et al., 2007; Schiller et al., 2020). Lebih jauh lagi, meskipun 83,86% klinisi mengetahui kontraindikasi NSAID pada dengue, hanya 11,21% yang memahami secara utuh penyesuaian obat rutin lansia PTM—seperti penghentian sementara Statin, Diuretik, dan Antikoagulan-saat terjadi fase kritis kebocoran plasma dengue (Herman et al., 2021; Tovar et al., 2024). Selain itu, efek samping edema perifer akibat Amlodipine (12,3% kasus) kerap disalahartikan sebagai Filariasis atau memicu prescribing cascade pemberian diuretik yang tidak perlu pada lansia (Liang et al., 2022; Savage et al., 2020; Sica, 2003), sedangkan batuk kering akibat Captopril kerap merancukan skrining TBC Paru (Dicpinigaitis, 2014).

1.2 Rumusan Masalah
Berdasarkan keempat permasalahan pada Subtema Healthcare di atas, rumusan masalah yang dijawab melalui inovasi ini adalah:
Bagaimana merancang platform web triase pra-fasilitas dan dasbor pemindaian rekam medis yang mampu menyaring kasus ringan dari rumah, menyiapkan kepatuhan puasa pra-laboratorium, serta mengotomasi pengisian data pasien guna mengatasi Puskesmas dan klinik yang kewalahan menghadapi antrian panjang, administrasi manual, dan pengelolaan data yang belum optimal?
Bagaimana menghadirkan platform web ringan berkapabilitas offline dengan pemetaan spasio-ekologis One Health, deteksi lesi kulit terkalibrasi Fitzpatrick IV-VI, dan pra-notifikasi ketersediaan obat guna membantu masyarakat di wilayah kepulauan dan pedalaman yang terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan?
Bagaimana menyediakan metode skrining mandiri berbasis proksi fisik tanpa alat medis dan kalkulator risiko kardiovaskular non-laboratorium melalui peramban web bagi kelompok usia produktif yang berisiko diabetes, hipertensi, atau penyakit kronis lain tetapi jarang memeriksakan diri?
Bagaimana membangun sistem pakar farmakovigilans pencegah interaksi obat dan deteksi dini 11 tanda bahaya (Red Flags) yang terhubung langsung ke ambulans darurat bagi keluarga yang merawat lansia dan kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, serta menjangkau bantuan sehari-hari agar kondisi lansia tidak memburuk tanpa terdeteksi?

1.3 Tujuan Inovasi
Selaras dengan rumusan masalah tersebut, tujuan pengembangan GardaMedika-Web adalah:
Mengatasi antrian Panjang dan Administrasi Manual di Puskesmas/Klinik: Menyaring kasus kompetensi SKDI 4A keperawatan mandiri (Rute Hijau), memberikan instruksi wajib puasa 10-12 jam sebelum ke FKTP (Rute Kuning), mengintegrasikan pendaftaran antrian Mobile JKN, serta mengotomasi injeksi data anamnesis ke RME Puskesmas melalui pemindaian QR Code berstandar SATUSEHAT HL7 FHIR R4 di Web Dashboard FKTP.
Menjembatani Hambatan Jarak dan Biaya Transportasi Masyarakat Kepulauan/Pedalaman: Menyediakan aplikasi web progresif (Progressive Web App) yang tetap berjalan tanpa sinyal internet stabil untuk mendeteksi penyakit endemis/NTD secara akurat pada kulit gelap (Fitzpatrick IV-VI) dan memastikan kesiapan stok logistik obat program nasional (MDT, OAT, Praziquantel) di Puskesmas tujuan sebelum warga menempuh perjalanan jauh.
Memfasilitasi Pemantauan Dini Penyakit Kronis yang Mudah Dijangkau bagi Usia Produktif: Menghadirkan fitur objektivikasi mandiri berbasis proksi antropometri-hemodinamik dan perhitungan risiko serangan jantung/stroke 10 tahun (WHO SEAR-B Non-Laboratory Chart) yang dapat diakses langsung via tautan web tanpa memerlukan alat ukur medis maupun tes darah laboratorium.
Memberdayakan Keluarga Perawat Lansia dalam Pemantauan Pengobatan dan Tanggap Darurat: Menghadirkan 5 Trigger Farmakovigilans Obat untuk mencegah komplikasi medikasi mandiri dan prescribing cascade pada lansia, serta mengintegrasikan penapisan 11 Red Flags langsung dengan panggilan darurat SPGDT PSC 119, Live Tracking ambulans, dan panduan visual Bantuan Hidup Dasar (BHD).

1.4 Landasan Regulasi dan Kepatuhan Hukum Nasional
Operasionalisasi sistem ini berpijak pada empat regulasi kesehatan nasional terkini:
Undang-Undang RI Nomor 17 Tahun 2023 tentang Kesehatan (Pasal 325): Memberikan legitimasi hukum pemanfaatan telemedisin dan kecerdasan buatan untuk kesinambungan perawatan (continuity of care) melalui mekanisme Regulatory Sandbox Kementerian Kesehatan RI (Pemerintah Republik Indonesia, 2023).
Peraturan Menteri Kesehatan RI Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit: Berlaku efektif 11 Maret 2026 (Berita Negara RI Tahun 2026 Nomor 173); mengonsolidasikan tata kelola Penyakit Menular tular vektor/zoonosis (Bab II Pasal 4, 25, 26), pendekatan Satu Kesehatan (One Health) (Bagian Kesepuluh), serta deteksi dini faktor risiko PTM melalui anamnesis, pemeriksaan fisik, dan penunjang (Bab III Pasal 42-43), sekaligus mengintegrasikan regulasi penanggulangan Kusta, Frambusia, dan Filariasis (Kemenkes RI, 2014, 2017a, 2019b, 2026).
Keputusan Menteri Kesehatan RI Nomor HK.01.07/MENKES/1186/2022 tentang PPK Dokter di FKTP: Mengklasifikasikan pengelolaan penyakit berdasarkan matriks kompetensi SKDI (Tingkat Kemampuan 4A, 3A, 3B, serta 1 dan 2) untuk menekan rujukan non-spesialistik ke rumah sakit (Kemenkes RI, 2022a).
Undang-Undang RI Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP) & Permenkes Nomor 24 Tahun 2022 tentang Rekam Medis: Mewajibkan perlindungan privasi data kesehatan sensitif dan interoperabilitas Rekam Medis Elektronik nasional (Kemenkes RI, 2022b; Pemerintah Republik Indonesia, 2022).






























BAB II KONSEP SOLUSI & KEUNGGULAN EKOSISTEM WEB SIKLUS TERTUTUP

2.1 Gambaran Umum Arsitektur Klinis 4 Lapisan (9 Tahap)
GardaMedika-Web beroperasi dalam siklus tertutup (closed-loop clinical architecture) yang memproses data pasien melalui 4 Lapisan Berurutan (Tahap 1 hingga Tahap 9):
Lapisan 1 - Filter Demografi Absolut, Keluhan Utama & Primary Survey Red Flags (Tahap 1-3): Menyaring variabel usia, jenis kelamin, dan kehamilan (Tahap 1), mengelompokkan 8 klaster sindromik keluhan utama (Tahap 2), dan memeriksa 11 indikator tanda bahaya primer (Tahap 3). Jika satu saja Red Flag terpenuhi, sistem mengaktifkan jalur pintas (bypass) langsung menuju Rute Merah (IGD & SPGDT PSC 119).
Lapisan 2 - Konteks Ekologi One Health, Keamanan Obat & Anamnesis HPI Dinamis (Tahap 4-5): Memetakan faktor risiko geospasial/lingkungan dan gaya hidup (Q4), menjalankan 5 aturan intervensi farmakovigilans pada obat yang sedang dikonsumsi pasien (Q5), serta menggali History of Present Illness (HPI) secara spesifik sesuai klaster terpilih untuk 32 entitas penyakit (Tahap 5).
Lapisan 3 - Objektivikasi Klinis Mandiri & Inferensi Multimodal (Tahap 6-7): Mengatasi ketiadaan alat ukur medis rumah tangga dengan menyediakan opsi input tanda vital/antropometri atau proksi fisik biostatistik (Q6 & Q7), deteksi visual lesi kulit terkalibrasi Fitzpatrick IV-VI dan sklera mata disertai aturan Multimodal Override (Q8), serta penghitungan skor risiko kardiovaskular WHO SEAR-B Non-Laboratory Chart dan aturan Vital Sign Override (Tahap 7).
Lapisan 4 - Orkestrasi 4 Rute Layanan & Interoperabilitas Nasional (Tahap 8-9): Mendistribusikan luaran ke Rute Hijau, Rute Kuning, Rute Kuning Khusus, atau Rute Merah (Tahap 8) yang terintegrasi dengan pendaftaran antrian Mobile JKN dan pemindaian QR Code SATUSEHAT HL7 FHIR R4 pada dasbor web Puskesmas/RS (Tahap 9) (Kemenkes RI & Dinas Kesehatan Provinsi Kalimantan Tengah, 2025).

2.2 Keunggulan Strategis Platform Berbasis Web (Web-First Clinical Ecosystem)
Pemilihan arsitektur berbasis Web Progresif (Progressive Web Application / PWA) dan Ekosistem Web Dua Sisi dibandingkan aplikasi native konvensional dirancang secara spesifik untuk menjawab keempat tantangan lapangan pada Subtema Healthcare:
Akses Instan Tanpa Hambatan Instalasi (Zero-Install Friction) saat Darurat Lansia & bagi Usia Produktif:
Keluarga yang menghadapi kondisi darurat lansia di rumah (seperti serangan stroke atau nyeri dada akut) tidak memiliki waktu untuk mengunduh dan menginstal aplikasi berukuran besar dari toko aplikasi. Demikian pula, kelompok usia produktif yang enggan memeriksakan diri seringkali malas menginstal aplikasi kesehatan khusus. Melalui platform web kami, pengguna cukup membuka satu tautan web melalui peramban ponsel apa pun (atau melalui tautan WhatsApp kader/Puskesmas) dan antarmuka triase langsung siap digunakan dalam waktu kurang dari 2 detik.
Komputasi Peramban Lokal (In-Browser Client-Side Inference) & Offline Caching untuk Kepulauan/Pedalaman:
Warga di wilayah kepulauan dan pedalaman sering kali menggunakan ponsel berspesifikasi rendah dengan ruang penyimpanan penuh serta sinyal internet yang terputus-putus. Platform web kami memanfaatkan Service Workers dan eksekusi model di sisi peramban klien (client-side web inference), sehingga setelah halaman web terbuka sekali, seluruh logika 9 tahap, deteksi kamera, dan kalkulator risiko dapat berjalan 100% offline tanpa koneksi internet serta tanpa membebani memori internal ponsel.
Ekosistem Web Dua Sisi (Dual-Sided Web Portal) untuk Dekongesti Administrasi Puskesmas/Klinik:
Solusi kami tidak hanya berhenti di layar ponsel pasien, melainkan menyediakan Web Dashboard Faskes (FKTP/IGD) yang dapat langsung dibuka melalui peramban komputer meja pendaftaran atau ruang dokter di Puskesmas tanpa perlu instalasi perangkat lunak tambahan pada infrastruktur IT Puskesmas. Petugas Puskesmas cukup mengarahkan kamera web (webcam) atau scanner ke QR Code SATUSEHAT HL7 FHIR R4 di layar ponsel pasien, dan seluruh ringkasan anamnesis, tanda vital, peringatan interaksi obat, serta rekomendasi laboratorium langsung tampil terstruktur dan siap diinjeksi ke dalam SIMPUS/RME dalam 1 detik (zero-retyping), sekaligus menampilkan notifikasi kedatangan pasien Rute Kuning Khusus (kesiapan ruang isolasi airborne & stok obat NTD/DOTS) maupun Rute Merah.
Privasi Medis Tingkat Tinggi (Client-Side Privacy-by-Design):
Seluruh pemrosesan citra klinis sensitif (foto lesi kulit kusta/skabies atau sklera mata) berlangsung di dalam memori peramban lokal (in-browser memory) tanpa pernah diunggah ke peladen awan (cloud server) pihak ketiga, menjamin kepatuhan mutlak terhadap UU PDP Nomor 27 Tahun 2022 (Pemerintah Republik Indonesia, 2022).

2.3 Matriks Keunggulan Kompetitif (Unique Value Proposition)
Parameter Inovasi
Aplikasi Telemedisin Native / Symptom Checker Biasa
GardaMedika-Web (Solusi Web yang Diajukan)
Aksesibilitas & Hambatan Pengguna
Wajib unduh/instal aplikasi puluhan MB; memerlukan koneksi internet terus-menerus.
Web Zero-Install (PWA) & Offline-Capable: Langsung diakses via browser di ponsel spesifikasi rendah tanpa kuota/sinyal stabil.
Dekongesti antrian & Administrasi Puskesmas
Hanya memberi saran teks konsultasi; petugas Puskesmas tetap mengetik ulang anamnesis manual dari nol.
Dual-Sided Web (Pasien & Faskes): Saring SKDI 4A di Rute Hijau, mandat puasa 10-12 jam di Rute Kuning, & Web Scanner QR Code HL7 FHIR R4 (zero-retyping RME).
Akses Kepulauan/Pedalaman & Geospasial One Health
Mengabaikan peta distribusi vektor/NTD lokal; warga pedalaman rawan salah rujuk ke faskes yang kosong obat.
Memetakan fokus endemis spesifik (28 desa Skistosomiasis, Indonesia Timur) & mengirim Web Pre-Notification stok obat NTD/DOTS ke dasbor Puskesmas.
Skrining Usia Produktif Tanpa Alat Ukur Medis
Gagal memprediksi risiko apabila pengguna tidak memiliki timbangan, meteran, tensimeter, atau hasil darah.
Mengonversi proksi fisik (celana menyempit / baju melonggar / rigors) & menghitung risiko jantung/stroke 10 tahun dengan WHO Non-Laboratory CVD Risk Chart (SEAR-B).
Pemantauan Lansia & Farmakovigilans Aktif
Tidak mendeteksi bahaya interaksi obat rutin terhadap infeksi akut maupun efek samping obat yang meniru NTD/TBC.
Dilengkapi 5 Trigger Keamanan Obat (cegah perdarahan NSAID-DBD, evaluasi Statin/Diuretik/Warfarin, serta bedakan edema Amlodipine vs. Filariasis dan batuk Captopril vs. TBC).












BAB III PROTOKOL KLINIS, PEMETAAN SPASIO-EKOLOGIS & ALGORITMA MEDIS (TAHAP 1-6)

3.1 Filter Demografi Absolut (Tahap 1), Keluhan Utama (Tahap 2), dan Primary Survey 11 Red Flags (Tahap 3)
Penyaringan variabel usia, jenis kelamin, dan status kehamilan pada Tahap 1 (Q1) memiliki justifikasi patofisiologis krusial. Dalam PNPK Infeksi Dengue Dewasa dan Anak, kehamilan, usia anak (<15 tahun yang rentan mengalami antibody-dependent enhancement / ADE), serta lansia dengan komorbiditas diklasifikasikan sebagai kondisi khusus (Group B Dengue) yang wajib dipantau di rumah sakit meskipun belum menunjukkan warning signs (Ikatan Dokter Anak Indonesia [IDAI], 2022; Kemenkes RI, 2020b, 2021b). Pada ibu hamil, sitokin pro-inflamasi dengue meningkatkan permeabilitas kapiler sistemik dan menstimulasi kontraksi miometrium yang berisiko memicu syok hipovolemik, solusio plasenta, persalinan prematur, hingga kematian maternal-perinatal (Federação Brasileira das Associações de Ginecologia e Obstetrícia [FEBRASGO], 2024; Paz-Bailey et al., 2024).

Setelah pengguna memilih satu dari 8 Klaster Keluhan Utama pada Tahap 2 (Q2) sesuai pendekatan sindromik PPK FKTP (Kemenkes RI, 2022a), sistem web mengeksekusi Primary Survey (Tahap 3 - Q3) berbasis prinsip ABCDE dan pedoman Emergency Triage Assessment and Treatment (ETAT) (World Health Organization [WHO], 2016):

Indikator Red Flag (Q3)
Entitas Klinis & Patofisiologi
Parameter Klinis, Ambang Batas Kritis & Sitasi Pedoman Resmi (APA 7)
1. Ikon Es / Tangan Dingin
Dengue Shock Syndrome (DSS) / Syok Hipovolemik
Muncul pada fase defervesensi (hari ke-3 s.d. ke-7): muntah persisten, nyeri perut hebat, ekstremitas dingin/lembap, nadi lemah/filiform, CRT >2 detik, tekanan nadi menyempit <20 mmHg, peningkatan hematokrit ≥20% (FEBRASGO, 2024; IDAI, 2022; Kemenkes RI, 2020b, 2021b; WHO, 2009, 2011).
2. Ikon Tetesan Darah
Perdarahan GI Masif / Hemoptisis Masif TBC
Epistaksis/gusi berdarah masif, hematemesis, atau melena akibat trombositopenia, disfungsi trombosit, dan koagulopati (penurunan fibrinogen & pemanjangan aPTT); atau batuk darah masif erosi arteri bronkialis TBC (Alam et al., 2022; Kemenkes RI, 2020b, 2022a; Tovar et al., 2024).
3. Ikon Toilet Disilang
Gagal Ginjal Akut (AKI) ec. Leptospirosis (Weil's Disease), Malaria Berat, atau DSS
Oliguria kuantitatif: produksi urin <0,5 mL/kg/jam (dewasa) atau <1,5 mL/kg/jam (anak/dengue berat) selama minimal 6 jam, atau anuria selama 6-8 jam akibat nekrosis tubular akut hipoperfusi/nefrotoksisitas (FEBRASGO, 2024; Kemenkes RI, 2023a; WHO, 2023).
4. Ikon Paru Biru / Sesak
Gagal Napas Akut, Pneumonia Berat, Campak Berat, Edema Paru
Retraksi dinding dada bawah (chest indrawing), stridor saat istirahat (obstruksi jalan napas atas / laringotrakeobronkitis campak), sianosis sentral, atau distres napas akibat efusi pleura/edema paru (Kemenkes RI, 2020b; Tovar et al., 2024; WHO, 2016).
5. Ikon Otak / Kejang
Ensefalopati Dengue, Malaria Serebral, Meningoensefalitis, Tifoid Toksik
Penurunan kesadaran (letargi, iritabilitas, koma), kejang, paresis, atau kaku kuduk akibat sekuestrasi eritrosit terinfeksi P. falciparum di mikrovaskular serebral, edema serebri, atau perdarahan intrakranial (FEBRASGO, 2024; Kemenkes RI, 2019c, 2020b; WHO, 2023).
6. Ikon Lemas Ekstrem
Dehidrasi Berat / Syok Gastroenteritis Akut
Minimal 2 tanda dehidrasi berat WHO: letargi/tidak sadar, mata sangat cekung, tidak bisa/malas minum, dan turgor kulit perut kembali sangat lambat (≥2 detik) (American Academy of Family Physicians [AAFP], 2022; WHO, 2005).
7. Ikon Gigitan Hewan
Luka GHPR Kategori III & Ensefalitis Rabies
Luka gigitan transdermal tunggal/multipel berdarah dari anjing, kera, atau kucing liar (Kategori III WHO memerlukan pencucian luka 15 menit, VAR, dan SAR), atau gejala patognomonik hidrofobia, fotofobia, dan hipersalivasi otonom (Kemenkes RI, 2026; WHO, 2018).
8. Ikon Jantung Petir
Sindrom Koroner Akut / Code STEMI
Angina tipikal berupa rasa tertekan/berat di substernal menjalar ke lengan kiri, leher, rahang, atau punggung >20 menit disertai gejala otonom diaforesis (keringat dingin), mual, atau sinkop (European Society of Cardiology [ESC], 2023; Perhimpunan Dokter Spesialis Kardiovaskular Indonesia [PERKI], 2025).
9. Ikon Wajah Mencong
Code Stroke Akut (Iskemik / Hemoragik)
Defisit neurologis fokal mendadak mengacu pada akronim BE-FAST atau slogan Kemenkes SeGeRa Ke RS (Senyum tidak simetris/mencong, Gerak separuh tubuh melemah tiba-tiba, bicaRa pelo/afasia) (Kemenkes RI, 2019c, 2024).
10. Ikon Kepala Kilat
Krisis Hipertensi (Hipertensi Emergensi / Ensefalopati)
Kenaikan tekanan darah ekstrem disertai kerusakan organ target akut (Hypertension-Mediated Organ Damage / HMOD) seperti retinopati/papiledema (pandangan mendadak gelap/kabur), iskemia serebral, atau edema pulmonal akut (Kemenkes RI, 2021a; PERKI, 2025).
11. Ikon Pingsan / Buah
Krisis Hiperglikemia (KAD & SHH) / Hipoglikemia Berat
Penurunan kesadaran, agitasi, tremor dan pucat diaforetik (neuroglikopenia hipoglikemia), atau pernapasan cepat dan dalam (Kussmaul) disertai napas berbau buah/aseton akibat ketonemia pada Ketoasidosis Diabetik (Kemenkes RI, 2020a; PERKENI, 2021, 2024).

3.2 Pemetaan Ekologi One Health (Tahap 4 - Q4) dan Sistem Pakar Farmakovigilans Obat (Tahap 4 - Q5)
Pada Tahap 4 (Q4), sistem mengintegrasikan determinan spasio-ekologis sesuai mandat One Health dalam Permenkes Nomor 3 Tahun 2026 (Kemenkes RI, 2026). Indikator paling spesifik adalah penapisan riwayat beraktivitas/berenang di Danau Lindu, Lembah Napu, atau Lembah Bada (Sulawesi Tengah) untuk mendeteksi Skistosomiasis (Schistosoma japonicum). Di Indonesia, penyakit ini hanya endemik di 28 desa pada ketiga dataran tinggi tersebut (Kabupaten Sigi dan Kabupaten Poso), dengan 242 daerah fokus keong amfibi Oncomelania hupensis lindoensis seluas 1.407.225m2 (Dinas Kesehatan Provinsi Sulawesi Tengah & Kemenkes RI, 2024; Widjaja et al., 2017). Meskipun prevalensi pada manusia di Lembah Napu sempat ditekan hingga 0,15%, laju infeksi pada reservoar mamalia liar (tikus) masih mencapai 16% di Lindu dan 7,3%-22,7% di Napu, sehingga reinfeksi terus terjadi saat warga bertani atau mencuci di saluran air fokus keong (Satrija et al., 2017; WHO Indonesia, 2023). Selain itu, Q4 memetakan riwayat perjalanan 1-4 bulan dari Indonesia Timur (Papua, Maluku, NTT) atau area tambang/hutan untuk Malaria dan Frambusia (Kemenkes RI, 2017a, 2026), paparan banjir/lumpur tikus untuk Leptospirosis, hunian padat (asrama/pesantren) dan kontak serumah pasien OAT untuk TBC, Skabies, Tinea, dan Hepatitis A (Hengge et al., 2007; Kamath et al., 2024; Kemenkes RI, 2022a), serta faktor risiko PTM (riwayat keluarga lini pertama, merokok, sedentari, dan diet tinggi purin/lemak jenuh) (Perhimpunan Reumatologi Indonesia [IRA], 2024; PERKI, 2025).

Pada Tahap 4 (Q5), sistem menerapkan 5 Aturan Pemicu Farmakovigilans (Medication Safety Triggers) untuk melindungi lansia dan pasien komorbid di rumah:
Trigger 1A (Suspek DBD + Kontraindikasi Absolut NSAID): Jika pasien demam mengonsumsi Ibuprofen, Aspirin (ASA), Natrium Diklofenak, atau Asam Mefenamat, sistem memunculkan Pop-up Merah untuk menghentikan NSAID seketika dan menggantinya dengan Paracetamol serta kompres hangat, karena inhibisi COX-1 pada kondisi trombositopenia dan koagulopati dengue memicu perdarahan gastrointestinal masif, perforasi, dan Sindrom Reye (Alam et al., 2022; Mohiuddin, 2023; Sharp et al., 2021; U.S. Centers for Disease Control and Prevention [U.S. CDC], 2024; U.S. National Library of Medicine [U.S. NLM], 2024c).
Sub-Trigger 1B (Suspek DBD + Evaluasi Obat Komorbid PTM): Mengingat hanya 11,21% klinisi memahami penyesuaian obat komorbid saat dengue akut (Herman et al., 2021), jika pasien lansia PTM yang mengalami demam akut mengonsumsi Statin (Simvastatin/Atorvastatin), Diuretik (Furosemide/HCT), atau Antikoagulan (Warfarin), sistem memberikan Pop-up Peringatan Kritis untuk evaluasi penghentian sementara oleh dokter guna mencegah perburukan hepatopati/miositis dengue (elevasi SGOT/SGPT & CK), kolaps kardiovaskular saat fase plasma leakage, serta perdarahan saluran cerna sinergis (Tovar et al., 2024).
Trigger 2 (Suspek Diare Akut / Disentri + Larangan Antimotilitas): Jika pasien diare mengonsumsi Loperamide, Attapulgite, atau Kaolin-Pektin, sistem memunculkan Pop-up Kuning untuk menghentikan obat tersebut dan beralih ke Oralit dan Zinc, karena agonis opioid mu menghambat peristaltik propulsif usus yang pada infeksi invasif (Shigella, Salmonella, Entamoeba histolytica) memicu kolitis amebik fulminan, toxic megacolon, perforasi kolon, serta aritmia ventrikel (QTc prolongation) pada anak di bawah 2 tahun (Chansrichavala et al., 2015; Grobusch et al., 2025; Koo et al., 2007; Schiller et al., 2020; U.S. NLM, 2024b, 2024d).
Trigger 3 (Efek Samping Amlodipine vs. Filariasis Limfatik): Amlodipine memicu edema perifer pitting bilateral lebih tinggi dibanding non-DHP CCB (12,3% vs. 3,1%; risiko 2,8x lipat pada dosis tinggi) akibat vasodilatasi selektif arteriol pre-kapiler tanpa diimbangi venula post-kapiler, berbeda dari limfedema Filariasis yang asimetris, non-pitting (fibrosis/hiperkeratosis), dan menetap >3 bulan (Ahmed et al., 2024; Largeau et al., 2021; Liang et al., 2022; Moffatt et al., 2003; Putri et al., 2025; Sica, 2003; Zheng et al., 2026). Pop-up Biru mencegah rujukan palsu ke Poli NTD sekaligus mencegah prescribing cascade pemberian diuretik yang tidak perlu pada lansia, sembari menyarankan evaluasi kombinasi ACEi/ARB di FKTP yang menurunkan risiko edema sebesar 38% (RR 0,62) (Makani et al., 2011; Savage et al., 2020).
Trigger 4 (Efek Samping Captopril/ACEi vs. Tuberkulosis Paru): Inhibisi enzim ACE (kininase II) oleh Captopril/Lisinopril menyebabkan akumulasi bradikinin dan substansi P di saluran napas yang mengiritasi serat C tanpa mielin, menghasilkan batuk kering persisten non-produktif tanpa demam (Dicpinigaitis, 2014; U.S. NLM, 2024a). Pop-up Biru memverifikasi ada tidaknya gejala konstitusional TBC sesuai algoritma 5 Pertanyaan Skrining TBC Kemenkes sebelum menyimpulkan suspek TBC Paru (Kemenkes RI, 2023b).

3.3 Protokol Anamnesis Mendalam Dinamis (Tahap 5) pada 32 Entitas Penyakit
Pada Tahap 5, antarmuka web memunculkan pertanyaan History of Present Illness (HPI) secara spesifik berdasarkan klaster terpilih untuk membedakan 32 entitas penyakit secara presisi:

Klaster HPI (Tahap 5)
Cakupan 32 Entitas Penyakit
Karakteristik Klinis Patognomonik pada Algoritma & Sitasi Pedoman (APA 7)
Klaster 1: Demam Vektor & Zoonosis
1. DBD & Syok Dengue (DSS)

2. Malaria & Malaria Serebral

3. Chikungunya Akut & Kronis

4. Leptospirosis & Weil's Disease

5. Skistosomiasis (Katayama)
• DBD: Demam bifasik pelana kuda (saddleback) turun hari ke-3/4 disertai letargi & nyeri retro-orbital; deteksi fase kritis mencegah DSS dengan mortalitas <0,5% (Kemenkes RI, 2020b, 2021b; WHO, 2011).

• Malaria: Paroksisme periodik 2-3 hari (menggigil-demam-berkeringat) (WHO, 2023).

• Leptospirosis: Demam naik-turun + nyeri tekan hebat otot betis gastrocnemius (Kemenkes RI, 2022a).

• Chikungunya Kronis: Artralgia melumpuhkan skala VAS ≥7 durasi >90 hari (Barrera et al., 2023; Sharp et al., 2021).

• Skistosomiasis: Riwayat gatal swimmer's itch (dermatitis serkaria) diikuti demam Sindrom Katayama 4-8 minggu kemudian (Satrija et al., 2017; Widjaja et al., 2017).
Klaster 2: Saluran Napas & Dada
6. ISPA Akut

7. TBC Paru/Ekstraparu & Hemoptisis

8. Pneumonia Berat / Gagal Napas
• ISPA Akut: Batuk akut <14 hari disertai rinitis dan faringitis (Kemenkes RI, 2022a).

• TBC Paru: Algoritma 5 Pertanyaan: batuk produktif/kronis ≥14 hari disertai diaforesis nokturnal (keringat malam basah kuyup tanpa aktivitas), anoreksia, penurunan BB, demam subfebris, atau hemoptisis (Kemenkes RI, 2019d, 2023b).

• Pneumonia Berat: Sesak napas berat, retraksi dada bawah, stridor istirahat, sianosis (WHO, 2016).
Klaster 3: Pencernaan & Hepatobilier
9. Diare Akut & Dehidrasi Berat

10. Amebiasis / Disentri

11. Demam Tifoid & Tifoid Toksik

12. Hepatitis Akut A & B

13. Cacingan (STH)
• Diare Akut vs. Amebiasis: Diare cair >3x/hari tanpa darah/lendir vs. disentri darah/lendir disertai tenesmus perih (AAFP, 2022; Kemenkes RI, 2022a; Koo et al., 2007).

• Demam Tifoid: Pola demam step-ladder memuncak malam hari + nyeri tekan abdomen (Kemenkes RI, 2022a).

• Hepatitis Akut A/B: Bilirubinuria warna teh gelap + nyeri kuadran kanan atas (Kemenkes RI, 2022a).

• Cacingan (STH): Anak usia 1-12 tahun dengan malnutrisi kurus-perut buncit, pruritus ani nokturnal, atau ekspulsi cacing (Kemenkes RI, 2017b).
Klaster 4: Kulit, Lesi Mukosa & Eksantema
14. Skabies

15. Tinea (Dermatofitosis)

16. Kusta (PB & MB)

17. Frambusia (Yaws)

18. Campak (Ringan & Berat)

19. Varicella (Ringan & Berat)
• Skabies vs. Tinea: Pruritus nokturnal sela jari/lipatan vs. plak eritematosa bersisik tepi aktif central clearing gatal saat berkeringat (Hengge et al., 2007; Kemenkes RI, 2022a).

• Kusta: Tanda Kardinal Pertama berupa makula hipopigmentasi/eritematosa yang mengalami mati rasa (baal/anestesi) saat diuji tusuk jarum atau penebalan saraf tepi (Kemenkes RI, 2019a, 2019b).

• Frambusia: Papiloma/koreng bergranulasi mirip buah raspberry (mother yaw) akibat invasi Treponema pallidum subsp. pertenue melalui abrasi kulit (Kemenkes RI, 2017a, 2026).

• Campak vs. Varicella: Ruam makulopapular didahului prodromal 3C (cough, coryza, conjunctivitis) vs. vesikel menyebar sentrifugal (Kemenkes RI, 2022a).
Klaster 5: Pembengkakan NTD
20. Filariasis Limfatik
• Filariasis Limfatik: Edema ekstremitas bawah kronis >3 bulan, bersifat asimetris, menetap, dan tidak mencekung saat ditekan jari (non-pitting edema) (Kemenkes RI, 2014, 2026; Moffatt et al., 2003).
Klaster 6: Gula & Saraf PTM
21. DM Tipe 2 Stabil/Katabolik

22. Krisis KAD/SHH & Hipoglikemia

23. Neuropati, Ulkus & Acanthosis
• DM Tipe 2 & Polineuropati: Trias klasik 3P (Poliuria, Polidipsia, Polifagia) disertai penurunan BB katabolik tanpa sebab jelas; parestesia/kebas bilateral simetris berpola kaos kaki (stocking-and-glove distribution) (Kemenkes RI, 2020a; PERKENI, 2021, 2024).
Klaster 7: Tekanan, Kepala & Vaskular PTM
24. Hipertensi Derajat 1 & 2

25. Krisis Hipertensi Emergensi

26. Angina Pektoris Stabil & STEMI

27. Dislipidemia

28. Stroke Akut
• Hipertensi & Angina Pektoris Stabil: Sakit kepala oksipital dan tengkuk berat/kaku; nyeri dada substernal atau sesak napas yang dipicu eksklusif oleh aktivitas fisik (naik tangga) dan mereda dengan istirahat (Perhimpunan Dokter Hipertensi Indonesia [InaSH], 2019; Kemenkes RI, 2021a; PERKI, 2025).
Klaster 8: Sendi PTM & Kegawatan Lain
29. Artritis Gout Akut & Tofus

30. Mialgia Ringan

(+31. Rabies & 32. Meningoensefalitis di Q3)
• Artritis Gout Akut: Serangan inflamasi sendi monoartikular mendadak pada sendi metatarsofalangeal pertama (jempol kaki / Podagra) dengan bengkak, eritema, teraba panas, dan nyeri tekan ekstrem yang mencapai puncak dalam <12-24 jam (IRA, 2024).


3.4 Objektivikasi Klinis Mandiri, Kalibrasi Fitzpatrick IV-VI & Skor Risiko CVD WHO SEAR-B (Tahap 6-7)
Untuk mengatasi kesenjangan kepemilikan instrumen diagnostik rumah tangga pada Laporan SKI 2023, Tahap 6 dan logika klinis Tahap 7 menjalankan tiga mekanisme objektivikasi mandiri di peramban web:
Proksi Hemodinamik (Q6) & Proksi Antropometri (Q7): Apabila pengguna tidak memiliki termometer, tensimeter, timbangan, atau pita meteran, sistem menyediakan opsi proksi fisik: (a) menggigil gemetar hebat (rigors) atau keringat basah kuyup sebagai proksi kurva demam tinggi, dan perabaan denyut nadi radialis cepat/kuat saat istirahat sebagai proksi takikardia; (b) pakaian atau celana menjadi sangat longgar dalam 1-2 bulan terakhir sebagai proksi hiperkatabolisme (IMT <18,5 kg/m²) yang meningkatkan probabilitas posterior TBC Paru, Cacingan STH, dan DM tipe 2 dekompensata; serta (c) celana terasa makin sempit di pinggang sebagai proksi obesitas sentral (mengacu pada rentang IMT normal dewasa Indonesia 18,5-22,9 kg/m² dan batas lingkar pinggang obesitas sentral ≥90 cm pada laki-laki serta ≥80 cm pada perempuan sesuai Kepmenkes 4634/2021 dan PERKENI 2024) yang menjadi prediktor sindrom metabolik dan keparahan klinis malaria P. falciparum (Kemenkes RI, 2021a, 2024; PERKENI, 2024).
Kalibrasi Klinis Citra Kulit Fitzpatrick IV-VI, Sklera Mata & Rule-Based Multimodal Override (Q8): Pengambilan citra lesi kulit melalui kamera web ponsel (ruam DBD/Campak, vesikel Varicella, bercak Kusta, borok Frambusia/Ulkus Diabetikum, Tofus Gout, dan Acanthosis Nigricans) dikalibrasi khusus untuk kulit sawo matang hingga gelap (Fitzpatrick IV-VI). Studi perintis pada 1.709 citra klinis pasien berkulit gelap dan uji lapangan aplikasi WHO Skin NTDs membuktikan sensitivitas klinis ~80%-88% pada NTD kulit dengan penyaringan uncertainty score 0,200 (WHO, 2022; Yotsu et al., 2023a, 2023b, 2025), sedangkan pemisahan piksel latar belakang pada dataset Fitzpatrick 17k mendongkrak akurasi tugas baru sebesar 43,3% dan memangkas ketimpangan Gini warna kulit sebesar 20,9% (Zhang et al., 2024). Namun, karena evaluasi independen membuktikan sensitivitas visual AI turun dari 87,2% pada kusta klasik menjadi 69,6% pada kusta reaksional/atipikal (Deps et al., 2025a, 2025b), sistem menerapkan Rule-Based Multimodal Override: hasil uji mandiri tusuk jarum yang positif mati rasa (baal) atau nyeri saraf tepi pada Tahap 5 wajib mengunci Rute Kuning Khusus meskipun skor kepercayaan kamera rendah. Untuk mata kuning (ikterus Hepatitis A/B) vs. conjunctival suffusion (Leptospirosis), pencitraan didasarkan pada kromatisitas sklera ambient-subtracted tanpa kartu kalibrasi warna eksternal (Outlaw et al., 2020; Wang et al., 2021, 2023).
WHO Non-Laboratory-Based CVD Risk Chart (SEAR-B) & Vital Sign Override (Tahap 7): Selaras dengan Pedoman Puskesmas Klaster 3 Kemenkes RI dan Kepmenkes 1186/2022, estimasi risiko 10 tahun kejadian kardiovaskular fatal/non-fatal (infark miokard/stroke) dihitung menggunakan WHO Non-Laboratory-Based CVD Risk Chart wilayah epidemiologi SEAR-B (Indonesia) berbasis 5 variabel tanpa tes darah: Usia (40-74 tahun), Jenis Kelamin, Status Merokok, Tekanan Darah Sistolik, dan IMT ke dalam 5 pita risiko (<5% Rute Hijau, 5%-<10%, 10%-<20%, 20%-<30%, dan ≥30%) (Gujarathi et al., 2025; Kemenkes RI, 2022a, 2024; Khanal et al., 2023; Rezaei et al., 2023). Dilengkapi aturan Cross-Validation Override: jika Suhu ≥39,5 °C (hiperpireksia) atau Tekanan Darah Sistolik ≥160 mmHg (ambang Hipertensi Derajat 2 yang mewajibkan inisiasi farmakoterapi antihipertensi segera oleh dokter FKTP dan skrining HMOD sesuai Pedoman PERKI 2025 dan Kepmenkes 4634/2021), sistem otomatis membatalkan Rute Hijau dan menaikkan prioritas ke Rute Kuning (Kemenkes RI, 2021a; PERKI, 2025).
BAB IV ARSITEKTUR SISTEM WEB, PEMODELAN KECERDASAN BUATAN & REKAYASA PERANGKAT LUNAK (TAHAP 7)

4.1 Arsitektur Ekosistem Web Progresif (PWA), Dual-Sided Web Dashboard, dan Tech Stack Keseluruhan

4.2 Pemodelan Machine Learning untuk Imputasi Proksi Antropometri dan Klasifikasi Gejala Tabular

4.3 Arsitektur Computer Vision Terkalibrasi Fitzpatrick IV-VI, Segmentasi Piksel Latar Belakang, dan Kromatisitas Sklera Digital

4.4 Rekayasa Rule Engine Deterministik, Multimodal Override, dan Inferensi Lokal di Peramban (In-Browser Client-Side Inference)

4.5 Keamanan Siber Web, Enkripsi Data Lokal (Privacy-by-Design), dan Pengujian Performa Sistem

























BAB V ORKESTRASI RUJUKAN BERJENJANG, SPGDT PSC 119 & INTEROPERABILITAS SATUSEHAT HL7 FHIR R4 (TAHAP 8-9)

5.1 Protokol Klinis dan Logistik pada Empat Rute Triase Berjenjang (Tahap 8)
Luaran triase pada Tahap 8 menerjemahkan matriks kompetensi SKDI dalam Kepmenkes 1186/2022 dan Permenkes Nomor 3 Tahun 2026 ke dalam empat rute operasional pada layar web pengguna dan dasbor web faskes (Kemenkes RI, 2022a, 2026):

Rute Triase (Tahap 8)
Spektrum Diagnosis (Infeksi, NTD, & PTM)
Tindakan Sistem Web, Logistik Obat & Pemeriksaan Penunjang
Protokol Pertolongan Pertama, Edukasi & Target Waktu Klinis
1. RUTE HIJAU

(Perawatan Mandiri / Apotek / Telemedisin)
ISPA Ringan, Diare Akut tanpa dehidrasi, Skabies, Tinea, Varicella Ringan, STH Ringan, Risiko PTM Rendah (Skor CVD SEAR-B <5%), Mialgia Ringan.
Navigasi peta web GPS ke Apotek untuk obat bebas/bebas terbatas (Oralit, Zinc, Paracetamol, Krim Miconazole) serta Krim Permethrin 5% melalui Apoteker (skema DOWA) atau e-resep telemedisin Mobile JKN; larangan mutlak rekomendasi antibiotik tanpa resep (Kemenkes RI, 2021c); tombol integrasi Mobile JKN.
Ventilasi jendela pagi hari & etika batuk (ISPA/TBC); dekontaminasi pakaian/selimut dengan air panas >60 °C (Skabies) (Hengge et al., 2007); pembatasan garam ≤1 sdt/hari, gula <4 sdm/hari, dan olahraga 150 menit/minggu (30-60 menit/hari, 3-5 hari/minggu) (Kemenkes RI, 2021a; PERKI, 2025).
2. RUTE KUNING

(FKTP Puskesmas / Klinik Pratama)
Infeksi: DBD fase demam biasa, Malaria tanpa komplikasi, Chikungunya akut, Demam Tifoid, Hepatitis A/B, Amebiasis, Leptospirosis dini, Varicella berat.

PTM: DM Tipe 2 Stabil, Hipertensi Derajat 1-2, Artritis Gout, Dislipidemia, Neuropati Diabetik.
Penerbitan QR Code Rujukan FKTP & integrasi tombol "Buat Janji / Daftar Poli" Mobile JKN; Pop-up Mandat Wajib Puasa 10-12 Jam (hanya minum air putih) malam hari sebelum pemeriksaan lab PTM (GDP, GD 2 Jam PP, Profil Lipid, Asam Urat, Ureum/Kreatinin, HbA1c) guna mencegah elevasi trigliserida kilomikron post-prandial dan pembatalan periksa darah lansia (PERKENI, 2024; PERKI & PERKENI, 2022), atau lab Infeksi (Darah Rutin serial, NS1, Apusan Darah, Tubex/Widal, Feses).
Pada Gout Akut: Kompres es lokal, larangan keras memijat sendi bengkak (karena manipulasi mekanis memobilisasi pelepasan kristal monosodium urate / MSU ke cairan sinovial dan memperhebat badai sitokin IL-1), serta hidrasi air putih >2 liter/hari (8-16 gelas/hari) guna mencegah urolitiasis asam urat (IRA, 2024).

Pada DBD: Hidrasi cairan isotonik/oralit 2-3 liter/hari & pantau warning signs (Kemenkes RI, 2020b).
3. RUTE KUNING KHUSUS

(Poli Program Nasional Kemenkes)
Tuberkulosis (TBC Paru/Ekstraparu), Kusta (PB/MB), Frambusia, Filariasis Limfatik, Skistosomiasis, Campak Ringan tanpa komplikasi.
Navigasi eksklusif ke Puskesmas penyelenggara Poli DOTS & Eradikasi NTD; Web Pre-Notification otomatis kesiapan Ruang Isolasi Infeksi Airborne (khusus TBC & Campak untuk cegah infeksi nosokomial di ruang tunggu) serta jaminan stok logistik OAT, Blister MDT Kusta (PB 6 blister dalam 6-9 bulan / MB 12 blister dalam 12-18 bulan), Azitromisin POPM Frambusia, dan 3 pot tinja metode Kato-Katz / Praziquantel (Badan Kebijakan Pembangunan Kesehatan [BKPK] Kemenkes RI, 2023; Kemenkes RI, 2017a, 2019a, 2019b, 2026).
Penggunaan masker bedah bagi suspek TBC/Campak sejak dari rumah untuk memutus rantai transmisi droplet/airborne; penapisan kontak serumah untuk pemberian kemoprofilaksis Rifampisin dosis tunggal pada Kusta (Kemenkes RI, 2019b) atau POPM Azitromisin sekampung halaman pada temuan kasus Frambusia disertai surveilans serologis 3 tahun (Kemenkes RI, 2017a).
4. RUTE MERAH

(IGD FKRTL & SPGDT PSC 119)
Infeksi: Syok Dengue (DSS), Malaria Serebral, AKI Leptospirosis, Pneumonia/Campak Berat dengan stridor, Ensefalitis Rabies, TBC Hemoptisis Masif.

PTM: STEMI, Stroke Akut, Krisis Hipertensi/Ensefalopati, Koma Diabetik (KAD/SHH/Hipoglikemia Berat).
Aktivasi sirene visual/audio di peramban web & tombol [Panggil Ambulans (119)] terhubung ke NCC / PSC 119; transmisi otomatis Pre-Arrival Tele-triage Data & koordinat GPS ke dasbor web SIMRS IGD rujukan; Live Tracking ambulans (Kemenkes RI, 2016).
Target Waktu Kritis: Door-to-Balloon / EKG <10 menit (STEMI); Door-to-Needle <30 menit dalam Golden Hour <4,5 jam (Trombolisis Stroke); Resusitasi Cairan <15 menit (DSS); penurunan MAP 25% pada 1 jam pertama (Krisis Hipertensi) (Kemenkes RI, 2019c, 2020b; PERKI, 2025).


5.2 Prosedur Aktivasi Darurat SPGDT PSC 119 dan Protokol Pertolongan Pertama (First Aid) Presisi
Integrasi tombol darurat [Panggil Ambulans (119)] dan pengiriman telemetri pra-fasilitas pada Rute Merah merupakan implementasi langsung dari Peraturan Menteri Kesehatan Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT) Pasal 5 ayat (3) dan Pasal 27 ayat (3) huruf b untuk mempercepat response time penanganan pra-fasilitas (Kemenkes RI, 2016). Sambil menunggu ambulans tiba melalui layar Live Tracking di peramban web, sistem memandu keluarga/pendamping pasien dengan instruksi visual Bantuan Hidup Dasar (BHD) yang telah dikalibrasi secara klinis:
Luka Gigitan Hewan Penular Rabies (GHPR): Mencuci luka gigitan dengan sabun di bawah air mengalir selama 15 menit tanpa henti sebelum diberangkatkan untuk mendapatkan Vaksin Anti Rabies (VAR) dan Serum Anti Rabies (SAR) (WHO, 2018).
Penurunan Kesadaran, Stroke Akut & Syok Dengue: Menerapkan larangan mutlak pemberian makanan atau minuman per oral (Nil Per Os / NPO) saat kesadaran menurun guna mencegah aspirasi paru. Pada pasien Stroke Akut dengan penurunan kesadaran, pasien diposisikan dalam posisi pemulihan miring (lateral recovery position) untuk menjaga patensi jalan napas (sedangkan elevasi kepala 30 derajat dikhususkan bagi pasien dengan peningkatan tekanan intrakranial yang jalan napasnya telah aman) (Kemenkes RI, 2019c). Pada pasien Syok Dengue (DSS), tindakan peninggian kaki (passive leg raising) hanya boleh dilakukan apabila pasien tidak mengalami sesak napas akibat efusi pleura masif atau edema paru akut (Kemenkes RI, 2020b; Tovar et al., 2024).

5.3 Standar Interoperabilitas RME SATUSEHAT HL7 FHIR R4 dan Mobile JKN (Tahap 9)
Untuk memangkas administrasi manual dan antrian di Puskesmas sesuai Permenkes Nomor 24 Tahun 2022 tentang Rekam Medis (masa retensi minimal 25 tahun) dan Pedoman Tata Kelola Rumah Sakit Bidang Operasional Kemenkes RI (Kemenkes RI, 2022b; Kemenkes RI & Dinas Kesehatan Provinsi Kalimantan Tengah, 2025), fitur pemindaian QR Code Handover pada Web Scanner Dashboard Puskesmas langsung menginjeksi data triase ke dalam SIMPUS/SIMRS menggunakan standar HL7 FHIR Release 4 (R4) SATUSEHAT tanpa entri ulang (zero-retyping):

Komponen Data pada QR Code Web
HL7 FHIR R4 Resource Standar SATUSEHAT
Sistem Kode / Terminologi Wajib Kemenkes RI
Implementasi Spesifik pada Dasbor Web RME Puskesmas / SIMRS
Identitas & Demografi Pasien (Tahap 1)
Patient & Encounter
NIK / IHS Number SATUSEHAT
Memetakan usia, jenis kelamin administratif (male/female), dan mengaitkan sesi triase mandiri dengan kunjungan fasyankes melalui Encounter.
Tanda Vital, Antropometri & Skor CVD (Tahap 6-7)
Observation (vital-signs & exam)
LOINC & UCUM (Satuan Ukur)
Mengkodekan Suhu tubuh (8310-5 dalam Cel), TD Sistolik (8480-6), TD Diastolik (8462-4), Tinggi Badan (8302-2), Berat Badan (29463-7), IMT (39156-5), Lingkar Pinggang (8280-0), serta Status Kehamilan (82810-3).
Keluhan Utama, HPI & Suspek Diagnosis (Tahap 2, 5, 8)
Condition (provisional / differential)
ICD-10 (Klaim JKN) & SNOMED-CT (Klinis)
Mengkodekan suspek penyakit ke ICD-10: J06 (ISPA akut), A91 (DBD), A15 (TBC Paru), A30 (Kusta), A66 (Frambusia), B65.2 (S. japonicum), E11 (DM Tipe 2), I10 (Hipertensi), M10 (Gout).
Riwayat Obat Rutin & Peringatan Interaksi (Tahap 4 - Q5)
MedicationStatement & DetectedIssue
KFA (Kamus Farmasi & Alat Kesehatan Kemenkes RI)
Mencatat konsumsi NSAID, Loperamide, Amlodipine, Captopril, Statin, Diuretik, atau Warfarin dengan kode presisi KFA agar RME dokter dan apoteker FKTP langsung menerima flag interaksi obat secara otomatis.
Rekomendasi Pemeriksaan Laboratorium (Tahap 8)
ServiceRequest (Laboratory procedure)
LOINC & SNOMED-CT
Mengirimkan draf pengantar pesanan lab (Darah Rutin, NS1, GDP, Profil Lipid, Asam Urat, Kreatinin, TCM TBC, Kato-Katz) beserta atribut patientInstruction berisi mandat puasa 10-12 jam.
Pendaftaran antrian Online & Rujukan (Tahap 8-9)
Appointment & ServiceRequest
API Web Service BPJS Kesehatan (Mobile JKN / PCare)
Menghubungkan tombol "Buat Janji / Daftar Poli" ke endpoint antrian FKTP terdaftar milik peserta JKN untuk memangkas hambatan administratif di Puskesmas.


5.4 Kepatuhan Mediko-Legal dan Perlindungan Data Pribadi
Selaras dengan Undang-Undang Nomor 17 Tahun 2023 tentang Kesehatan dan Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (Pemerintah Republik Indonesia, 2022, 2023), pemrosesan citra klinis sensitif (seperti foto lesi kusta, frambusia, atau skabies pada Q8) dijalankan di memori peramban lokal perangkat pengguna tanpa diunggah ke peladen awan pihak ketiga, sedangkan transmisi data ke SATUSEHAT, Mobile JKN, atau PSC 119 hanya dieksekusi berdasarkan persetujuan sah (explicit informed consent) pasien atau dalam kondisi darurat penyelamatan nyawa pada Rute Merah. Layar hasil wajib menampilkan penafian mediko-legal bahwa luaran aplikasi web adalah alat bantu triase awal (Clinical Decision Support / Triage Tool) dan bukan diagnosis medis final maupun pengganti pemeriksaan fisik dan laboratorium oleh dokter.






BAB VI DAMPAK SISTEMIK, KEBERLANJUTAN & PETA JALAN IMPLEMENTASI

6.1 Matriks Dampak Terukur (Key Performance Indicators) terhadap Subtema Healthcare

Permasalahan pada Subtema Healthcare
Solusi Spesifik pada GardaMedika-Web
Target Indikator Kinerja Utama (KPI)
1. Puskesmas dan klinik kewalahan menghadapi antrian panjang, administrasi manual, serta pengelolaan data pasien yang belum optimal.
• Penyaringan kasus ringan (SKDI 4A) ke Rute Hijau.

• Pop-up wajib puasa 10-12 jam di Rute Kuning.

• One-click booking Mobile JKN & pindaian QR Code pada Web Scanner Dashboard Puskesmas berstandar SATUSEHAT HL7 FHIR R4.
• Penurunan beban antrian kasus ringan di FKTP >30%.

• 0% pembatalan cek lab lansia/PTM akibat lupa berpuasa.

• Pemangkasan waktu anamnesis & entri manual RME >50% (zero-retyping).
2. Masyarakat di wilayah kepulauan dan pedalaman terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan.
• Arsitektur Web PWA Zero-Install & Offline-Capable yang berjalan ringan tanpa sinyal internet stabil.

• Pemetaan spasio-ekologis One Health & deteksi NTD kulit Fitzpatrick IV-VI.

• Web Pre-Notification kesiapan stok obat (MDT, OAT, Praziquantel) di Rute Kuning Khusus.
• 100% ketersediaan fungsi triase di area blank-spot tanpa makan memori ponsel.

• Penghematan biaya transportasi warga pedalaman dengan mencegah perjalanan sia-sia ke faskes yang kosong logistik obat NTD/DOTS.
3. Usia produktif berisiko diabetes/hipertensi/penyakit kronis lain tetapi jarang memeriksakan diri, sehingga membutuhkan pemantauan dini yang mudah dijangkau.
• Akses skrining instan 1 klik via tautan peramban web.

• Imputasi proksi fisik (celana menyempit / baju melonggar) untuk mengatasi ketiadaan alat ukur (data SKI 2023).

• Kalkulasi risiko 10 tahun WHO Non-Laboratory CVD Risk Chart (SEAR-B).
• Menjangkau 35%-80% populasi dewasa yang belum memiliki alat ukur medis di rumah.

• Skrining dini PTM tuntas dalam <3 menit dari rumah tanpa instalasi aplikasi dan tanpa sampel darah.
4. Keluarga yang merawat lansia kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, dan menjangkau bantuan sehari-hari.
• 5 Trigger Farmakovigilans Obat (Q5) untuk memantau efek samping & interaksi obat rutin lansia.

• Deteksi 11 Red Flags, tombol darurat PSC 119, Live Tracking, dan panduan visual BHD langsung di peramban.
• 0 kasus perdarahan iatrogenik NSAID-DBD & eliminasi prescribing cascade Amlodipine.

• Pencapaian target Door-to-Balloon <10 menit, Door-to-Needle <30 menit, dan resusitasi syok <15 menit.


6.2 Strategi Implementasi Ekosistem Nasional & Keberlanjutan (Sustainability)
Pengujian Regulatory Sandbox DTO Kemenkes RI: Memanfaatkan kerangka UU Nomor 17 Tahun 2023 untuk menguji keamanan klinis, audit keadilan algoritma lintas warna kulit Fitzpatrick, dan sertifikasi standar HL7 FHIR R4 SATUSEHAT (Pemerintah Republik Indonesia, 2023).
Integrasi B2G (Business-to-Government) pada Ekosistem Web Puskesmas Klaster 3 & Mobile JKN: Karena berbasis web standar terbuka, sistem ini dapat langsung disematkan (embedded webview / direct link) ke dalam ekosistem BPJS Kesehatan serta dibuka langsung di komputer seluruh Puskesmas di Indonesia tanpa biaya pengadaan perangkat keras baru.
Efisiensi Biaya Komputasi (Near-Zero Cloud Inference Cost): Pemrosesan inferensi di peramban perangkat pengguna (client-side) menekan biaya operasional peladen pusat (cloud server) hingga >85%, memastikan keberlanjutan finansial jangka panjang.
6.3 Peta Jalan Pengembangan (Development Roadmap)
Fase 1 - Hackathon Web MVP & Validasi In-Silico (Bulan 1-3): Pembangunan antarmuka Patient Self-Triage Web (PWA) 9 Tahap dan FKTP Web Scanner Dashboard, integrasi mesin aturan 11 Red Flags (Q3) dan 5 Trigger Farmakovigilans (Q5), pemodelan machine learning & computer vision (Bab IV), serta generator/pemindai QR Code JSON HL7 FHIR R4.
Fase 2 - Regulatory Sandbox & Uji Validasi Klinis Prospektif (Bulan 4-6): Uji konkordansi hasil triase sistem web terhadap diagnosis dokter FKTP di Puskesmas perkotaan serta Puskesmas daerah endemis NTD (Sulawesi Tengah dan Indonesia Timur).
Fase 3 - Integrasi Ekosistem Nasional (Bulan 7-12): Koneksi endpoint produksi API SATUSEHAT Kemenkes RI, Web Service antrian Online Mobile JKN / PCare BPJS Kesehatan, dan sistem dispatch NCC / PSC 119 Kabupaten/Kota.



























DAFTAR PUSTAKA

Ahmed, S., et al. (2024). Case report: Escitalopram-associated lower limb edema and differential diagnosis of drug-associated lower limb edema. Frontiers in Psychiatry, 15, Article 1394813. https://doi.org/10.3389/fpsyt.2024.1394813
Alam, S. M., Qasswal, M., Ahsan, M. J., Walters, R. W., & Chandra, S. (2022). Selective serotonin reuptake inhibitors increase risk of upper gastrointestinal bleeding when used with NSAIDs: A systemic review and meta-analysis. Scientific Reports, 12(1), Article 14452. https://doi.org/10.1038/s41598-022-18654-2
American Academy of Family Physicians. (2022). Acute diarrhea in adults: Evaluation and management clinical guideline. American Family Physician, 106(1), 72-80. https://www.aafp.org/afp/2022/0700/acute-diarrhea
Badan Kebijakan Pembangunan Kesehatan Kementerian Kesehatan Republik Indonesia. (2023). Pedoman pengendalian schistosomiasis dan pemeriksaan laboratorium metode Kato-Katz. Kementerian Kesehatan Republik Indonesia.
Barrera, R., et al. (2023). Dengue, chikungunya and Zika arbovirus infections in Caribbean and tropical regions (PMCID: PMC10090388). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC10090388/
Chansrichavala, P., et al. (2015). Loperamide therapy for voluminous diarrhea in infectious disease settings (PMCID: PMC4366607). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC4366607/
Deps, P., Amorim, B. B. C., Repsold, T., & Almonfrey, D. (2025a). Independent assessment of the World Health Organization Skin Neglected Tropical Diseases application for leprosy detection (PMID: 42006576; PMCID: PMC13086047). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC13086047/
Deps, P., et al. (2025b). Artificial intelligence and integrated management of skin-related neglected tropical diseases. British Journal of Dermatology, 193(Suppl. 1), Article ljaf212. https://doi.org/10.1093/bjd/ljaf212
Dicpinigaitis, P. V. (2014). ACE inhibitors: Upper respiratory symptoms, bradykinin accumulation, and differential diagnosis. BMJ Case Reports, 2014, Article bcr2014205462. https://doi.org/10.1136/bcr-2014-205462
Dinas Kesehatan Provinsi Sulawesi Tengah & Kementerian Kesehatan Republik Indonesia. (2024). Schistosomiasis di Sulawesi Tengah: Epidemiologi, penularan, dan intervensi 2019-2024. Dinas Kesehatan Provinsi Sulawesi Tengah. https://dinkes.sultengprov.go.id/schistosomiasis-di-sulawesi-tengah-epidemiologi-penularan-dan-intervensi-2019-2024/
European Society of Cardiology. (2023). 2023 ESC Guidelines for the management of acute coronary syndromes. European Heart Journal, 44(38), 3720-3826. https://doi.org/10.1093/eurheartj/ehad191
Federação Brasileira das Associações de Ginecologia e Obstetrícia. (2024). Prevention, diagnosis, and treatment protocol of dengue during pregnancy and the postpartum period. Revista Brasileira de Ginecologia e Obstetrícia, 46, Article e-rbgo73. https://doi.org/10.61622/rbgo/2024rbgo73
Grobusch, M. P., et al. (2025). Racecadotril versus loperamide for acute diarrhea of infectious origin (PMCID: PMC12098968). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC12098968/
Gujarathi, A. P., Powar, J., Patil, R., Padhyegurjar, S., Ghodake, A. K., & Shaikh, M. H. M. A. (2025). Estimation of cardiovascular risk by using WHO/ISH charts and Correlation & Regression Tree (CART) analysis in adults of rural North Maharashtra, India. National Journal of Community Medicine, 16(11), 1101-1108. https://doi.org/10.55489/njcm.161120255801
Hengge, U. R., Currie, B. J., Jäger, G., Lupi, O., & Schwartz, R. A. (2007). Scabies: A ubiquitous neglected skin disease. Trends in Parasitology, 23(10), 485-493. https://doi.org/10.1016/j.pt.2007.08.007
Herman, L., et al. (2021). Assessment of knowledge, attitudes, and practices regarding dengue and NSAID contraindications among healthcare practitioners (PMCID: PMC8389296). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC8389296/
Ikatan Dokter Anak Indonesia. (2022). Pedoman nasional pelayanan kedokteran & konsensus tata laksana infeksi dengue anak dan remaja. Badan Penerbit Ikatan Dokter Anak Indonesia. https://www.idai.or.id/professional-resources/pedoman-konsensus/pedoman-nasional-pelayanan-kedokteran-tata-laksana-infeksi-dengue-anak-dan-remaja
Jones, O. T., Matin, R. N., van der Schaar, M., Prathivadi Bhayankaram, K., Ranmuthu, C. K. I., Islam, M. S., Behiyat, D., Boscott, R., Calanzani, N., Emery, J., Williams, H. C., & Walter, F. M. (2022). Artificial intelligence and machine learning algorithms for early detection of skin cancer in community and primary care settings: A systematic review. The Lancet Digital Health, 4(6), e466-e476. https://doi.org/10.1016/S2589-7500(22)00023-1
Kamath, S., et al. (2024). Using artificial intelligence on dermatology conditions in Uganda: Epidemiology and burden of tropical skin diseases (PMCID: PMC10782289). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC10782289/
Kementerian Kesehatan Republik Indonesia. (2014). Peraturan Menteri Kesehatan Republik Indonesia Nomor 94 Tahun 2014 tentang Penanggulangan Filariasis (Berita Negara Republik Indonesia Tahun 2014 Nomor 2036). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2016). Peraturan Menteri Kesehatan Republik Indonesia Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT). Direktorat Pelayanan Kesehatan Rujukan Kementerian Kesehatan Republik Indonesia. https://keslan.kemkes.go.id/lakip_files/direktorat_pelayanan_kesehatan_rujukan_rak_2021.pdf
Kementerian Kesehatan Republik Indonesia. (2017a). Peraturan Menteri Kesehatan Republik Indonesia Nomor 8 Tahun 2017 tentang Eradikasi Frambusia (Berita Negara Republik Indonesia Tahun 2017 Nomor 351). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/111971/permenkes-no-8-tahun-2017
Kementerian Kesehatan Republik Indonesia. (2017b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 15 Tahun 2017 tentang Penanggulangan Cacingan (Berita Negara Republik Indonesia Tahun 2017 Nomor 438). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2019a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/308/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tatalaksana Kusta. Kementerian Kesehatan Republik Indonesia. https://ayosehat.kemkes.go.id/topik-penyakit/pencegahan-infeksi-pada-usia-produktif/kusta
Kementerian Kesehatan Republik Indonesia. (2019b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 11 Tahun 2019 tentang Penanggulangan Kusta (Berita Negara Republik Indonesia Tahun 2019 Nomor 449). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/138606/permenkes-no-11-tahun-2019
Kementerian Kesehatan Republik Indonesia. (2019c). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/394/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Stroke (beserta Pedoman PERDOSSI). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2019d). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/755/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Tuberkulosis (beserta Pedoman PDPI). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2020a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/603/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Diabetes Melitus Tipe 2 Dewasa. Kementerian Kesehatan Republik Indonesia. https://rsudhaulussymaluku.com/unduh/4
Kementerian Kesehatan Republik Indonesia. (2020b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/9845/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue pada Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.kemkes.go.id/eng/pnpk-2020---tata-laksana-infeksi-dengue-pada-dewasa
Kementerian Kesehatan Republik Indonesia. (2021a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4634/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Hipertensi Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.prescribingcompanion.com/indonesia/kondisi-klinis-umum-lainnya/f-kardiovaskular/6-hipertensi-esensial/
Kementerian Kesehatan Republik Indonesia. (2021b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4636/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue Anak dan Remaja. Kementerian Kesehatan Republik Indonesia. http://www.kemkes.go.id/id/pnpk-2021---infeksi-dengue-anak-dan-remaja
Kementerian Kesehatan Republik Indonesia. (2021c). Peraturan Menteri Kesehatan Republik Indonesia Nomor 28 Tahun 2021 tentang Pedoman Penggunaan Antibiotik (Berita Negara Republik Indonesia Tahun 2021 Nomor 1076). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2022a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1186/2022 tentang Panduan Praktik Klinis bagi Dokter di Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP). Kementerian Kesehatan Republik Indonesia. https://manuver.tireg7.net/wp-content/uploads/2025/01/KEPMENKES-HK-01-07-MENKES-1186-2022-2.pdf
Kementerian Kesehatan Republik Indonesia. (2022b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis (Berita Negara Republik Indonesia Tahun 2022 Nomor 829). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2023a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1634/2023 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Penyakit Ginjal Kronik. Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2023b). Petunjuk teknis kolaborasi TBC-HIV. Direktorat Jenderal Pencegahan dan Pengendalian Penyakit Kementerian Kesehatan Republik Indonesia. https://kemkes.go.id/
Kementerian Kesehatan Republik Indonesia. (2024). Pedoman kerja Puskesmas klaster 3: Kesehatan usia dewasa dan lanjut usia (Memuat statistik Survei Kesehatan Indonesia / SKI 2023 dan tabel prediksi risiko PTM adaptasi WHO Cardiovascular Disease Risk Charts). Kementerian Kesehatan Republik Indonesia. https://renbut.kemkes.go.id/regulasi/Pedoman%20Puskesmas%20Klaster%203.pdf
Kementerian Kesehatan Republik Indonesia & Dinas Kesehatan Provinsi Kalimantan Tengah. (2025). Pedoman tata kelola rumah sakit: Buku 4 bidang operasional (Standar interoperabilitas SATUSEHAT HL7 FHIR R4 dan pengkodean LOINC). Kementerian Kesehatan Republik Indonesia. https://dinkes.kalteng.go.id/wp-content/uploads/2025/10/Pedoman-Tata-Kelola-Rumah-Sakit-Buku-4-Bidang-Operasional.pdf
Kementerian Kesehatan Republik Indonesia. (2026). Peraturan Menteri Kesehatan Republik Indonesia Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit (Berita Negara Republik Indonesia Tahun 2026 Nomor 173). Biro Hukum Kementerian Kesehatan Republik Indonesia. https://peraturan.go.id/files/permenkes-no-3-tahun-2026.pdf
Khanal, P., et al. (2023). Estimation of 10-year cardiovascular risk among adult population in western Nepal using nonlaboratory-based WHO/ISH chart, 2023: A cross-sectional study. Health Science Reports, 6(10), Article e1614. https://doi.org/10.1002/hsr2.1614
Koo, H. L., DuPont, H. L., & Musher, D. M. (2007). Fulminant amoebic colitis following loperamide use. Journal of Travel Medicine, 14(1), 61-62. https://doi.org/10.1111/j.1708-8305.2006.00095.x
Largeau, B., Cracowski, J. L., Lengellé, C., Sautenet, B., & Jonville-Béra, A. P. (2021). Drug-induced peripheral oedema: An aetiology-based review. British Journal of Clinical Pharmacology, 87(8), 3043-3055. https://doi.org/10.1111/bcp.14752
Liang, L., Kung, J. Y., Mitchelmore, B., Cave, A., & Banh, H. L. (2022). Comparative peripheral edema for dihydropyridines calcium channel blockers treatment: A systematic review and network meta-analysis. The Journal of Clinical Hypertension, 24(5), 536-554. https://doi.org/10.1111/jch.14436
Makani, H., Bangalore, S., Romero, J., Htyte, N., Berrios, R. S., Makwana, H., & Messerli, F. H. (2011). Peripheral edema associated with calcium channel blockers: Incidence and withdrawal rate—a meta-analysis of randomized trials. Journal of Hypertension, 29(7), 1270-1280. https://doi.org/10.1097/HJH.0b013e3283472643
Moffatt, C. J., Franks, P. J., Doherty, D. C., Williams, A. F., Badger, C., Jeffs, E., Bosanquet, N., & Mortimer, P. S. (2003). Lymphoedema: An underestimated health problem. QJM: An International Journal of Medicine, 96(10), 731-738. https://doi.org/10.1093/qjmed/hcg126
Mohiuddin, A. K. (2023). Erroneous uses of NSAIDs in patients with COVID-19, dengue, and chikungunya. Universal Journal of Pharmacy and Pharmacology, 2(1), 1-2. https://doi.org/10.31586/ujpp.2023.551
Outlaw, F., Meek, J., MacDonald, L. W., & Leung, T. S. (2020). Smartphone screening for neonatal jaundice via ambient-subtracted scleral chromaticity. PLOS One, 15(3), Article e0216970. https://pmc.ncbi.nlm.nih.gov/articles/PMC7051077/
Paz-Bailey, G., Adams, L. E., Deen, J., Anderson, K. B., & Katzelnick, L. C. (2024). Dengue. JAMA, 331(10), 874-884. https://doi.org/10.1001/jama.2023.27724
Pemerintah Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196). Sekretariat Negara Republik Indonesia.
Pemerintah Republik Indonesia. (2023). Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan (Lembaran Negara Republik Indonesia Tahun 2023 Nomor 105). Sekretariat Negara Republik Indonesia. https://gudangilmu.farmasetika.com/bab-ii-transformasi-teknologi-kesehatan-blueprint/
Perhimpunan Dokter Hipertensi Indonesia. (2019). Konsensus penatalaksanaan hipertensi di Indonesia (Tabel prediksi risiko PTM diadaptasi dari WHO Cardiovascular Disease Risk Charts). Perhimpunan Dokter Hipertensi Indonesia (InaSH). https://www.inash.or.id/
Perhimpunan Dokter Spesialis Kardiovaskular Indonesia & Perkumpulan Endokrinologi Indonesia. (2022). Panduan tata laksana dislipidemia di Indonesia. Pengurus Pusat PERKI & PB PERKENI.
Perhimpunan Dokter Spesialis Kardiovaskular Indonesia. (2025). Pedoman tatalaksana hipertensi pada penyakit kardiovaskular & sindrom koroner akut. Pengurus Pusat Perhimpunan Dokter Spesialis Kardiovaskular Indonesia (PERKI). https://www.inaheart.org/wp-content/uploads/2025/10/Pedoman-Tatalaksana-Hipertensi-Pada-Penyakit-Kardiovaskular.pdf
Perhimpunan Reumatologi Indonesia. (2024). Pedoman diagnosis dan tatalaksana hiperurisemia & artritis gout (Edisi pembaruan; ISBN: 978-979-3730-48-6). Pengurus Besar Perhimpunan Reumatologi Indonesia (IRA). https://reumatologi.or.id/wp-content/uploads/2024/09/ISBN-Hiperurisemia-Artritis-Gout_download.pdf
Perkumpulan Endokrinologi Indonesia. (2021). Pedoman petunjuk praktis terapi insulin pada pasien diabetes melitus tahun 2021. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://papdisolo.com/library
Perkumpulan Endokrinologi Indonesia. (2024). Pedoman pengelolaan dan pencegahan diabetes melitus tipe 2 dewasa di Indonesia tahun 2024. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://pbperkeni.or.id/wp-content/uploads/2025/08/DMT2-2024-Protected.pdf
Putri, R. A., et al. (2025). Pengaruh penggunaan amlodipine terhadap risiko edema perifer pada pasien hipertensi. Jurnal Sains dan Kesehatan, 7(3), 213-221. https://doi.org/10.25026/jsk.v7i3.2460
Rezaei, F., Seif, M., Fattahi, M. R., Gandomkar, A., & Hasanzadeh, J. (2023). Comparison of laboratory-based and non-laboratory-based WHO cardiovascular disease risk charts: A population-based study. The Lancet Diabetes & Endocrinology, 11(7), 480-490. https://doi.org/10.1016/S2213-8587(23)00119-5
Satrija, F., Ridwan, Y., Jastal, Samarang, & Rauf, A. (2017). Current status of schistosomiasis in Indonesia: Epidemiology, transmission, and integrated control. Infectious Diseases of Poverty, 6(1), 1-14. https://doi.org/10.1186/s40249-017-0256-8
Savage, R. D., Visentin, J. D., Bronskill, S. E., Wang, X., Gruneir, A., Giannakeas, V., Guan, J., Lam, K., Luke, M. J., Read, S. H., Stall, N. M., Wu, W., Zhu, L., Rochon, P. A., & McCarthy, L. M. (2020). Evaluation of a common prescribing cascade of calcium channel blockers and diuretics in older adults with hypertension. JAMA Internal Medicine, 180(5), 643-651. https://doi.org/10.1001/jamainternmed.2019.7087
Schiller, L. R., et al. (2020). Severe acute diarrhea: Pathophysiology, antimotility contraindications, and management (PMCID: PMC7127018). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC7127018/
Sharp, T. M., Keating, M. K., Shieh, W. J., Bhatnagar, J., Bollweg, B. C., Levine, R., Blau, D. M., Torres, J. V., Rivera, A., Perez-Padilla, J., Munoz-Jordan, J., Sanabria, D., Fischer, M., & Zaki, S. R. (2021). Clinical characteristics, histopathology, and tissue immunolocalization of chikungunya and dengue virus infections. Clinical Infectious Diseases, 73(2), e345-e354. https://doi.org/10.1093/cid/ciaa837
Sica, D. A. (2003). Calcium channel blocker-related peripheral edema: Can it be resolved? The Journal of Clinical Hypertension, 5(4), 291-295. https://doi.org/10.1111/j.1524-6175.2003.02402.x
Tovar, J. H., Pinzón, M. A., Rincón, D. F., et al. (2024). Anesthesia and perioperative care management in patients with dengue fever: Coagulopathy, plasma leakage, and comorbid medications. Brazilian Journal of Anesthesiology, 74(4), Article 844521. https://pmc.ncbi.nlm.nih.gov/articles/PMC11233874/
U.S. Centers for Disease Control and Prevention. (2024). CDC clinical guidance for dengue & contraindication of NSAIDs. U.S. Department of Health and Human Services.
U.S. National Library of Medicine, National Institutes of Health. (2024a). Angiotensin-converting enzyme inhibitors (ACEI) (StatPearls Bookshelf ID: NBK431051). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK431051/
U.S. National Library of Medicine, National Institutes of Health. (2024b). DailyMed official drug monograph: Loperamide hydrochloride capsule (SetID: 1be585e2-ef49-4210-8a2d-22a326e4cc1b). National Institutes of Health. https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1be585e2-ef49-4210-8a2d-22a326e4cc1b
U.S. National Library of Medicine, National Institutes of Health. (2024c). Ibuprofen (StatPearls Bookshelf ID: NBK542299). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK542299/
U.S. National Library of Medicine, National Institutes of Health. (2024d). Loperamide (StatPearls Bookshelf ID: NBK557885). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK557885/
Wang, L., et al. (2021). Neonatal jaundice detection using a computer vision system. Designs, 5(4), Article 63. https://doi.org/10.3390/designs5040063
Wang, Y., et al. (2023). Non-invasive and non-contact automatic jaundice detection of neonates and adults using computer vision. Computer Methods in Biomechanics and Biomedical Engineering: Imaging & Visualization, 11(6), Article 2244601. https://doi.org/10.1080/21681163.2023.2244601
Widjaja, J., Anastasia, H., Nurwidayati, A., Nurjana, M. A., Mujiyanto, & Maksud, M. (2017). Situasi terkini daerah fokus keong hospes perantara di daerah endemis schistosomiasis di Sulawesi Tengah. Buletin Penelitian Kesehatan, 45(4), 215-222. https://doi.org/10.22435/bpk.v45i4.7570.215-222
World Health Organization. (2005). The treatment of diarrhoea: A manual for physicians and other senior health workers (4th rev., beserta Pedoman Lintas Diare Kemenkes RI). World Health Organization.
World Health Organization. (2009). Dengue: Guidelines for diagnosis, treatment, prevention and control (New ed.). World Health Organization. https://www.who.int/publications/i/item/9789241547871
World Health Organization, Regional Office for South-East Asia. (2011). Comprehensive guidelines for prevention and control of dengue and dengue haemorrhagic fever (Revised and expanded ed.). World Health Organization. https://iris.who.int/handle/10665/204894
World Health Organization. (2016). Updated guideline: Paediatric emergency triage, assessment and treatment (ETAT) (beserta Buku Bagan MTBS Kemenkes RI). World Health Organization.
World Health Organization. (2018). WHO expert consultation on rabies: Third report (beserta Petunjuk Teknis Penatalaksanaan Kasus GHPR Kemenkes RI). World Health Organization.
World Health Organization. (2022). Ending the neglect to attain the Sustainable Development Goals: A strategic framework for integrated control and management of skin-related neglected tropical diseases. World Health Organization. https://www.who.int/publications/i/item/9789240051423
World Health Organization. (2023). WHO guidelines for malaria (beserta PNPK Tata Laksana Malaria Kemenkes RI). World Health Organization.
World Health Organization Indonesia. (2023, July 25). Overcoming challenges to eliminate schistosomiasis in Central Sulawesi (Mengatasi tantangan untuk mengeliminasi schistosomiasis di Sulawesi Tengah). World Health Organization. https://www.who.int/indonesia/id/news/detail/25-07-2023-overcoming-challenges-to-eliminate-schistosomiasis-in-central-sulawesi
Yotsu, R. R., Ding, Z., Hamm, J., & Blanton, R. E. (2023a). Deep learning for AI-based diagnosis of skin-related neglected tropical diseases: A pilot study. PLOS Neglected Tropical Diseases, 17(8), Article e0011230. https://doi.org/10.1371/journal.pntd.0011230
Yotsu, R. R., et al. (2023b). Integrated control and management of skin-related neglected tropical diseases. PLOS Neglected Tropical Diseases, 17(6), Article e0011357. https://doi.org/10.1371/journal.pntd.0011357
Yotsu, R. R., Oiwoh, S. O., Mbali, H., Parajuli, N., Enbiale, W., & Ruiz-Postigo, J. A. (2025). Harnessing artificial intelligence for skin-related neglected tropical diseases (skin NTDs): Opportunities, challenges and future directions. International Health, 17(5), 792-794. https://doi.org/10.1093/inthealth/ihaf068
Zhang, H., et al. (2024). Robust visual identification of under-resourced dermatological conditions: Background pixel separation on the Fitzpatrick 17k dataset in lower and middle income countries (PMCID: PMC12099365). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC12099365/
Zheng, X., et al. (2026). Incidence and risk factors of calcium channel blocker-related edema in hypertensive patients: A multicenter retrospective cohort study. PLOS One, 21(3), Article e0336659. https://doi.org/10.1371/journal.pone.0336659
COVER








































DAFTAR ISI

BAB I PENDAHULUAN	4
1.1 Latar Belakang dan Validasi Masalah	4
1.2 Rumusan Masalah	5
1.3 Tujuan Inovasi	6
1.4 Landasan Regulasi dan Kepatuhan Hukum Nasional	6
BAB II KONSEP SOLUSI & KEUNGGULAN EKOSISTEM WEB SIKLUS TERTUTUP	8
2.1 Gambaran Umum Arsitektur Klinis 4 Lapisan (9 Tahap)	8
2.2 Keunggulan Strategis Platform Berbasis Web (Web-First Clinical Ecosystem)	8
2.3 Matriks Keunggulan Kompetitif (Unique Value Proposition)	9
BAB III PROTOKOL KLINIS, PEMETAAN SPASIO-EKOLOGIS & ALGORITMA MEDIS (TAHAP 1-6)	11
3.1 Filter Demografi Absolut (Tahap 1), Keluhan Utama (Tahap 2), dan Primary Survey 11 Red Flags (Tahap 3)	11
3.2 Pemetaan Ekologi One Health (Tahap 4 - Q4) dan Sistem Pakar Farmakovigilans Obat (Tahap 4 - Q5)	14
3.3 Protokol Anamnesis Mendalam Dinamis (Tahap 5) pada 32 Entitas Penyakit	15
3.4 Objektivikasi Klinis Mandiri, Kalibrasi Fitzpatrick IV-VI & Skor Risiko CVD WHO SEAR-B (Tahap 6-7)	19
BAB IV ARSITEKTUR SISTEM WEB, PEMODELAN KECERDASAN BUATAN & REKAYASA PERANGKAT LUNAK (TAHAP 7)	21
4.1 Arsitektur Ekosistem Web Progresif (PWA), Dual-Sided Web Dashboard, dan Tech Stack Keseluruhan	21
4.2 Pemodelan Machine Learning untuk Imputasi Proksi Antropometri dan Klasifikasi Gejala Tabular	21
4.3 Arsitektur Computer Vision Terkalibrasi Fitzpatrick IV-VI, Segmentasi Piksel Latar Belakang, dan Kromatisitas Sklera Digital	21
4.4 Rekayasa Rule Engine Deterministik, Multimodal Override, dan Inferensi Lokal di Peramban (In-Browser Client-Side Inference)	21
4.5 Keamanan Siber Web, Enkripsi Data Lokal (Privacy-by-Design), dan Pengujian Performa Sistem	21
BAB V ORKESTRASI RUJUKAN BERJENJANG, SPGDT PSC 119 & INTEROPERABILITAS SATUSEHAT HL7 FHIR R4 (TAHAP 8-9)	22
5.1 Protokol Klinis dan Logistik pada Empat Rute Triase Berjenjang (Tahap 8)	22
5.2 Prosedur Aktivasi Darurat SPGDT PSC 119 dan Protokol Pertolongan Pertama (First Aid) Presisi	25
5.3 Standar Interoperabilitas RME SATUSEHAT HL7 FHIR R4 dan Mobile JKN (Tahap 9)	26
5.4 Kepatuhan Mediko-Legal dan Perlindungan Data Pribadi	28
BAB VI DAMPAK SISTEMIK, KEBERLANJUTAN & PETA JALAN IMPLEMENTASI	29
6.1 Matriks Dampak Terukur (Key Performance Indicators) terhadap Subtema Healthcare	29
6.2 Strategi Implementasi Ekosistem Nasional & Keberlanjutan (Sustainability)	30
6.3 Peta Jalan Pengembangan (Development Roadmap)	31
DAFTAR PUSTAKA	32



































BAB I PENDAHULUAN

1.1 Latar Belakang dan Validasi Masalah
Transformasi layanan kesehatan primer di Indonesia masih menghadapi empat hambatan struktural dari tingkat rumah tangga hingga Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP):
Penumpukan antrian, Administrasi Manual, dan Pengelolaan Data yang Belum Optimal di Puskesmas/Klinik:
Puskesmas dan klinik kewalahan menghadapi antrian yang panjang, administrasi manual, serta pengelolaan data pasien yang belum optimal. Secara operasional dan klinis, masalah ini dipicu oleh tiga faktor: (a) masuknya kasus ringan tanpa komplikasi (Tingkat Kemampuan 4A pada Standar Kompetensi Dokter Indonesia / SKDI) yang seharusnya tuntas melalui perawatan mandiri di rumah (Kemenkes RI, 2022a); (b) batalnya pemeriksaan laboratorium ribuan pasien PTM/lansia di Puskesmas karena datang dalam kondisi sudah sarapan (post-prandial), padahal pemeriksaan Gula Darah Puasa (GDP) dan Profil Lipid mewajibkan puasa 8 hingga 12 jam (Perkumpulan Endokrinologi Indonesia [PERKENI], 2024); serta (c) beban pencatatan anamnesis berulang secara manual oleh tenaga medis ke dalam sistem Rekam Medis Elektronik (RME).
Kendala Jarak, Biaya Transportasi, dan Bias Deteksi di Wilayah Kepulauan serta Pedalaman:
Masyarakat di wilayah kepulauan dan pedalaman terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan. Di wilayah berkembang, rasio dokter terhadap pasien dapat mencapai 1:25.000 dengan kelangkaan ekstrem dokter spesialis dermatologi, padahal penyakit kulit menempati urutan keempat penyebab disabilitas non-fatal global (Years Lived with Disability) (Kamath et al., 2024). Ketika warga di daerah endemis (seperti Papua, Maluku, NTT, atau 28 desa endemis Skistosomiasis di Sulawesi Tengah) mengalami demam tropis atau lesi kulit NTD, kesalahan mengunjungi fasilitas yang tidak memiliki stok obat program nasional (MDT Kusta, OAT, Azitromisin POPM, atau Praziquantel) menyebabkan pemborosan biaya transportasi yang berat. Di sisi lain, algoritma kecerdasan buatan dermatologi konvensional yang dilatih pada kulit terang (Fitzpatrick I-III) mengalami penurunan kinerja tajam saat diterapkan pada populasi tropis berkulit sawo matang hingga gelap (Fitzpatrick IV-VI) (Jones et al., 2022).
Rendahnya Pemeriksaan Rutin dan Kebutuhan Pemantauan Dini pada Usia Produktif:
Usia produktif yang berisiko diabetes, hipertensi, atau penyakit kronis lain jarang memeriksakan diri, sehingga membutuhkan cara pemantauan dini yang lebih mudah dijangkau. Laporan Survei Kesehatan Indonesia (SKI) 2023 membuktikan bahwa secara nasional 80,82% penduduk dewasa tidak pernah mengukur lingkar perut, 62,6% tidak pernah memeriksa kadar gula darah, 61,6% tidak pernah memeriksa kolesterol, dan 35,61% tidak memantau berat badan, sementara prevalensi hipertensi dan diabetes meningkat signifikan mulai usia 40 tahun ke atas (p<0,01) dan prevalensi TBC usia produktif (25-34 tahun) mencapai 0,42% (Kemenkes RI, 2024; Khanal et al., 2023).
Kesulitan Pemantauan Lansia, Risiko Obat Mandiri, dan Keterlambatan Akses Bantuan Darurat:
Keluarga yang merawat lansia kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, dan menjangkau bantuan sehari-hari, sehingga kondisi lansia berisiko memburuk tanpa terdeteksi. Di masyarakat, swamedikasi obat anti-nyeri NSAID (Ibuprofen/Aspirin) pada demam dengue memicu perdarahan saluran cerna masif (Alam et al., 2022; Mohiuddin, 2023), sedangkan penggunaan antimotilitas (Loperamide) pada disentri memicu kolitis fulminan dan toxic megacolon (Koo et al., 2007; Schiller et al., 2020). Lebih jauh lagi, meskipun 83,86% klinisi mengetahui kontraindikasi NSAID pada dengue, hanya 11,21% yang memahami secara utuh penyesuaian obat rutin lansia PTM—seperti penghentian sementara Statin, Diuretik, dan Antikoagulan-saat terjadi fase kritis kebocoran plasma dengue (Herman et al., 2021; Tovar et al., 2024). Selain itu, efek samping edema perifer akibat Amlodipine (12,3% kasus) kerap disalahartikan sebagai Filariasis atau memicu prescribing cascade pemberian diuretik yang tidak perlu pada lansia (Liang et al., 2022; Savage et al., 2020; Sica, 2003), sedangkan batuk kering akibat Captopril kerap merancukan skrining TBC Paru (Dicpinigaitis, 2014).

1.2 Rumusan Masalah
Berdasarkan keempat permasalahan pada Subtema Healthcare di atas, rumusan masalah yang dijawab melalui inovasi ini adalah:
Bagaimana merancang platform web triase pra-fasilitas dan dasbor pemindaian rekam medis yang mampu menyaring kasus ringan dari rumah, menyiapkan kepatuhan puasa pra-laboratorium, serta mengotomasi pengisian data pasien guna mengatasi Puskesmas dan klinik yang kewalahan menghadapi antrian panjang, administrasi manual, dan pengelolaan data yang belum optimal?
Bagaimana menghadirkan platform web ringan berkapabilitas offline dengan pemetaan spasio-ekologis One Health, deteksi lesi kulit terkalibrasi Fitzpatrick IV-VI, dan pra-notifikasi ketersediaan obat guna membantu masyarakat di wilayah kepulauan dan pedalaman yang terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan?
Bagaimana menyediakan metode skrining mandiri berbasis proksi fisik tanpa alat medis dan kalkulator risiko kardiovaskular non-laboratorium melalui peramban web bagi kelompok usia produktif yang berisiko diabetes, hipertensi, atau penyakit kronis lain tetapi jarang memeriksakan diri?
Bagaimana membangun sistem pakar farmakovigilans pencegah interaksi obat dan deteksi dini 11 tanda bahaya (Red Flags) yang terhubung langsung ke ambulans darurat bagi keluarga yang merawat lansia dan kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, serta menjangkau bantuan sehari-hari agar kondisi lansia tidak memburuk tanpa terdeteksi?

1.3 Tujuan Inovasi
Selaras dengan rumusan masalah tersebut, tujuan pengembangan GardaMedika-Web adalah:
Mengatasi antrian Panjang dan Administrasi Manual di Puskesmas/Klinik: Menyaring kasus kompetensi SKDI 4A keperawatan mandiri (Rute Hijau), memberikan instruksi wajib puasa 10-12 jam sebelum ke FKTP (Rute Kuning), mengintegrasikan pendaftaran antrian Mobile JKN, serta mengotomasi injeksi data anamnesis ke RME Puskesmas melalui pemindaian QR Code berstandar SATUSEHAT HL7 FHIR R4 di Web Dashboard FKTP.
Menjembatani Hambatan Jarak dan Biaya Transportasi Masyarakat Kepulauan/Pedalaman: Menyediakan aplikasi web progresif (Progressive Web App) yang tetap berjalan tanpa sinyal internet stabil untuk mendeteksi penyakit endemis/NTD secara akurat pada kulit gelap (Fitzpatrick IV-VI) dan memastikan kesiapan stok logistik obat program nasional (MDT, OAT, Praziquantel) di Puskesmas tujuan sebelum warga menempuh perjalanan jauh.
Memfasilitasi Pemantauan Dini Penyakit Kronis yang Mudah Dijangkau bagi Usia Produktif: Menghadirkan fitur objektivikasi mandiri berbasis proksi antropometri-hemodinamik dan perhitungan risiko serangan jantung/stroke 10 tahun (WHO SEAR-B Non-Laboratory Chart) yang dapat diakses langsung via tautan web tanpa memerlukan alat ukur medis maupun tes darah laboratorium.
Memberdayakan Keluarga Perawat Lansia dalam Pemantauan Pengobatan dan Tanggap Darurat: Menghadirkan 5 Trigger Farmakovigilans Obat untuk mencegah komplikasi medikasi mandiri dan prescribing cascade pada lansia, serta mengintegrasikan penapisan 11 Red Flags langsung dengan panggilan darurat SPGDT PSC 119, Live Tracking ambulans, dan panduan visual Bantuan Hidup Dasar (BHD).

1.4 Landasan Regulasi dan Kepatuhan Hukum Nasional
Operasionalisasi sistem ini berpijak pada empat regulasi kesehatan nasional terkini:
Undang-Undang RI Nomor 17 Tahun 2023 tentang Kesehatan (Pasal 325): Memberikan legitimasi hukum pemanfaatan telemedisin dan kecerdasan buatan untuk kesinambungan perawatan (continuity of care) melalui mekanisme Regulatory Sandbox Kementerian Kesehatan RI (Pemerintah Republik Indonesia, 2023).
Peraturan Menteri Kesehatan RI Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit: Berlaku efektif 11 Maret 2026 (Berita Negara RI Tahun 2026 Nomor 173); mengonsolidasikan tata kelola Penyakit Menular tular vektor/zoonosis (Bab II Pasal 4, 25, 26), pendekatan Satu Kesehatan (One Health) (Bagian Kesepuluh), serta deteksi dini faktor risiko PTM melalui anamnesis, pemeriksaan fisik, dan penunjang (Bab III Pasal 42-43), sekaligus mengintegrasikan regulasi penanggulangan Kusta, Frambusia, dan Filariasis (Kemenkes RI, 2014, 2017a, 2019b, 2026).
Keputusan Menteri Kesehatan RI Nomor HK.01.07/MENKES/1186/2022 tentang PPK Dokter di FKTP: Mengklasifikasikan pengelolaan penyakit berdasarkan matriks kompetensi SKDI (Tingkat Kemampuan 4A, 3A, 3B, serta 1 dan 2) untuk menekan rujukan non-spesialistik ke rumah sakit (Kemenkes RI, 2022a).
Undang-Undang RI Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP) & Permenkes Nomor 24 Tahun 2022 tentang Rekam Medis: Mewajibkan perlindungan privasi data kesehatan sensitif dan interoperabilitas Rekam Medis Elektronik nasional (Kemenkes RI, 2022b; Pemerintah Republik Indonesia, 2022).






























BAB II KONSEP SOLUSI & KEUNGGULAN EKOSISTEM WEB SIKLUS TERTUTUP

2.1 Gambaran Umum Arsitektur Klinis 4 Lapisan (9 Tahap)
GardaMedika-Web beroperasi dalam siklus tertutup (closed-loop clinical architecture) yang memproses data pasien melalui 4 Lapisan Berurutan (Tahap 1 hingga Tahap 9):
Lapisan 1 - Filter Demografi Absolut, Keluhan Utama & Primary Survey Red Flags (Tahap 1-3): Menyaring variabel usia, jenis kelamin, dan kehamilan (Tahap 1), mengelompokkan 8 klaster sindromik keluhan utama (Tahap 2), dan memeriksa 11 indikator tanda bahaya primer (Tahap 3). Jika satu saja Red Flag terpenuhi, sistem mengaktifkan jalur pintas (bypass) langsung menuju Rute Merah (IGD & SPGDT PSC 119).
Lapisan 2 - Konteks Ekologi One Health, Keamanan Obat & Anamnesis HPI Dinamis (Tahap 4-5): Memetakan faktor risiko geospasial/lingkungan dan gaya hidup (Q4), menjalankan 5 aturan intervensi farmakovigilans pada obat yang sedang dikonsumsi pasien (Q5), serta menggali History of Present Illness (HPI) secara spesifik sesuai klaster terpilih untuk 32 entitas penyakit (Tahap 5).
Lapisan 3 - Objektivikasi Klinis Mandiri & Inferensi Multimodal (Tahap 6-7): Mengatasi ketiadaan alat ukur medis rumah tangga dengan menyediakan opsi input tanda vital/antropometri atau proksi fisik biostatistik (Q6 & Q7), deteksi visual lesi kulit terkalibrasi Fitzpatrick IV-VI dan sklera mata disertai aturan Multimodal Override (Q8), serta penghitungan skor risiko kardiovaskular WHO SEAR-B Non-Laboratory Chart dan aturan Vital Sign Override (Tahap 7).
Lapisan 4 - Orkestrasi 4 Rute Layanan & Interoperabilitas Nasional (Tahap 8-9): Mendistribusikan luaran ke Rute Hijau, Rute Kuning, Rute Kuning Khusus, atau Rute Merah (Tahap 8) yang terintegrasi dengan pendaftaran antrian Mobile JKN dan pemindaian QR Code SATUSEHAT HL7 FHIR R4 pada dasbor web Puskesmas/RS (Tahap 9) (Kemenkes RI & Dinas Kesehatan Provinsi Kalimantan Tengah, 2025).

2.2 Keunggulan Strategis Platform Berbasis Web (Web-First Clinical Ecosystem)
Pemilihan arsitektur berbasis Web Progresif (Progressive Web Application / PWA) dan Ekosistem Web Dua Sisi dibandingkan aplikasi native konvensional dirancang secara spesifik untuk menjawab keempat tantangan lapangan pada Subtema Healthcare:
Akses Instan Tanpa Hambatan Instalasi (Zero-Install Friction) saat Darurat Lansia & bagi Usia Produktif:
Keluarga yang menghadapi kondisi darurat lansia di rumah (seperti serangan stroke atau nyeri dada akut) tidak memiliki waktu untuk mengunduh dan menginstal aplikasi berukuran besar dari toko aplikasi. Demikian pula, kelompok usia produktif yang enggan memeriksakan diri seringkali malas menginstal aplikasi kesehatan khusus. Melalui platform web kami, pengguna cukup membuka satu tautan web melalui peramban ponsel apa pun (atau melalui tautan WhatsApp kader/Puskesmas) dan antarmuka triase langsung siap digunakan dalam waktu kurang dari 2 detik.
Komputasi Peramban Lokal (In-Browser Client-Side Inference) & Offline Caching untuk Kepulauan/Pedalaman:
Warga di wilayah kepulauan dan pedalaman sering kali menggunakan ponsel berspesifikasi rendah dengan ruang penyimpanan penuh serta sinyal internet yang terputus-putus. Platform web kami memanfaatkan Service Workers dan eksekusi model di sisi peramban klien (client-side web inference), sehingga setelah halaman web terbuka sekali, seluruh logika 9 tahap, deteksi kamera, dan kalkulator risiko dapat berjalan 100% offline tanpa koneksi internet serta tanpa membebani memori internal ponsel.
Ekosistem Web Dua Sisi (Dual-Sided Web Portal) untuk Dekongesti Administrasi Puskesmas/Klinik:
Solusi kami tidak hanya berhenti di layar ponsel pasien, melainkan menyediakan Web Dashboard Faskes (FKTP/IGD) yang dapat langsung dibuka melalui peramban komputer meja pendaftaran atau ruang dokter di Puskesmas tanpa perlu instalasi perangkat lunak tambahan pada infrastruktur IT Puskesmas. Petugas Puskesmas cukup mengarahkan kamera web (webcam) atau scanner ke QR Code SATUSEHAT HL7 FHIR R4 di layar ponsel pasien, dan seluruh ringkasan anamnesis, tanda vital, peringatan interaksi obat, serta rekomendasi laboratorium langsung tampil terstruktur dan siap diinjeksi ke dalam SIMPUS/RME dalam 1 detik (zero-retyping), sekaligus menampilkan notifikasi kedatangan pasien Rute Kuning Khusus (kesiapan ruang isolasi airborne & stok obat NTD/DOTS) maupun Rute Merah.
Privasi Medis Tingkat Tinggi (Client-Side Privacy-by-Design):
Seluruh pemrosesan citra klinis sensitif (foto lesi kulit kusta/skabies atau sklera mata) berlangsung di dalam memori peramban lokal (in-browser memory) tanpa pernah diunggah ke peladen awan (cloud server) pihak ketiga, menjamin kepatuhan mutlak terhadap UU PDP Nomor 27 Tahun 2022 (Pemerintah Republik Indonesia, 2022).

2.3 Matriks Keunggulan Kompetitif (Unique Value Proposition)
Parameter Inovasi
Aplikasi Telemedisin Native / Symptom Checker Biasa
GardaMedika-Web (Solusi Web yang Diajukan)
Aksesibilitas & Hambatan Pengguna
Wajib unduh/instal aplikasi puluhan MB; memerlukan koneksi internet terus-menerus.
Web Zero-Install (PWA) & Offline-Capable: Langsung diakses via browser di ponsel spesifikasi rendah tanpa kuota/sinyal stabil.
Dekongesti antrian & Administrasi Puskesmas
Hanya memberi saran teks konsultasi; petugas Puskesmas tetap mengetik ulang anamnesis manual dari nol.
Dual-Sided Web (Pasien & Faskes): Saring SKDI 4A di Rute Hijau, mandat puasa 10-12 jam di Rute Kuning, & Web Scanner QR Code HL7 FHIR R4 (zero-retyping RME).
Akses Kepulauan/Pedalaman & Geospasial One Health
Mengabaikan peta distribusi vektor/NTD lokal; warga pedalaman rawan salah rujuk ke faskes yang kosong obat.
Memetakan fokus endemis spesifik (28 desa Skistosomiasis, Indonesia Timur) & mengirim Web Pre-Notification stok obat NTD/DOTS ke dasbor Puskesmas.
Skrining Usia Produktif Tanpa Alat Ukur Medis
Gagal memprediksi risiko apabila pengguna tidak memiliki timbangan, meteran, tensimeter, atau hasil darah.
Mengonversi proksi fisik (celana menyempit / baju melonggar / rigors) & menghitung risiko jantung/stroke 10 tahun dengan WHO Non-Laboratory CVD Risk Chart (SEAR-B).
Pemantauan Lansia & Farmakovigilans Aktif
Tidak mendeteksi bahaya interaksi obat rutin terhadap infeksi akut maupun efek samping obat yang meniru NTD/TBC.
Dilengkapi 5 Trigger Keamanan Obat (cegah perdarahan NSAID-DBD, evaluasi Statin/Diuretik/Warfarin, serta bedakan edema Amlodipine vs. Filariasis dan batuk Captopril vs. TBC).












BAB III PROTOKOL KLINIS, PEMETAAN SPASIO-EKOLOGIS & ALGORITMA MEDIS (TAHAP 1-6)

3.1 Filter Demografi Absolut (Tahap 1), Keluhan Utama (Tahap 2), dan Primary Survey 11 Red Flags (Tahap 3)
Penyaringan variabel usia, jenis kelamin, dan status kehamilan pada Tahap 1 (Q1) memiliki justifikasi patofisiologis krusial. Dalam PNPK Infeksi Dengue Dewasa dan Anak, kehamilan, usia anak (<15 tahun yang rentan mengalami antibody-dependent enhancement / ADE), serta lansia dengan komorbiditas diklasifikasikan sebagai kondisi khusus (Group B Dengue) yang wajib dipantau di rumah sakit meskipun belum menunjukkan warning signs (Ikatan Dokter Anak Indonesia [IDAI], 2022; Kemenkes RI, 2020b, 2021b). Pada ibu hamil, sitokin pro-inflamasi dengue meningkatkan permeabilitas kapiler sistemik dan menstimulasi kontraksi miometrium yang berisiko memicu syok hipovolemik, solusio plasenta, persalinan prematur, hingga kematian maternal-perinatal (Federação Brasileira das Associações de Ginecologia e Obstetrícia [FEBRASGO], 2024; Paz-Bailey et al., 2024).

Setelah pengguna memilih satu dari 8 Klaster Keluhan Utama pada Tahap 2 (Q2) sesuai pendekatan sindromik PPK FKTP (Kemenkes RI, 2022a), sistem web mengeksekusi Primary Survey (Tahap 3 - Q3) berbasis prinsip ABCDE dan pedoman Emergency Triage Assessment and Treatment (ETAT) (World Health Organization [WHO], 2016):

Indikator Red Flag (Q3)
Entitas Klinis & Patofisiologi
Parameter Klinis, Ambang Batas Kritis & Sitasi Pedoman Resmi (APA 7)
1. Ikon Es / Tangan Dingin
Dengue Shock Syndrome (DSS) / Syok Hipovolemik
Muncul pada fase defervesensi (hari ke-3 s.d. ke-7): muntah persisten, nyeri perut hebat, ekstremitas dingin/lembap, nadi lemah/filiform, CRT >2 detik, tekanan nadi menyempit <20 mmHg, peningkatan hematokrit ≥20% (FEBRASGO, 2024; IDAI, 2022; Kemenkes RI, 2020b, 2021b; WHO, 2009, 2011).
2. Ikon Tetesan Darah
Perdarahan GI Masif / Hemoptisis Masif TBC
Epistaksis/gusi berdarah masif, hematemesis, atau melena akibat trombositopenia, disfungsi trombosit, dan koagulopati (penurunan fibrinogen & pemanjangan aPTT); atau batuk darah masif erosi arteri bronkialis TBC (Alam et al., 2022; Kemenkes RI, 2020b, 2022a; Tovar et al., 2024).
3. Ikon Toilet Disilang
Gagal Ginjal Akut (AKI) ec. Leptospirosis (Weil's Disease), Malaria Berat, atau DSS
Oliguria kuantitatif: produksi urin <0,5 mL/kg/jam (dewasa) atau <1,5 mL/kg/jam (anak/dengue berat) selama minimal 6 jam, atau anuria selama 6-8 jam akibat nekrosis tubular akut hipoperfusi/nefrotoksisitas (FEBRASGO, 2024; Kemenkes RI, 2023a; WHO, 2023).
4. Ikon Paru Biru / Sesak
Gagal Napas Akut, Pneumonia Berat, Campak Berat, Edema Paru
Retraksi dinding dada bawah (chest indrawing), stridor saat istirahat (obstruksi jalan napas atas / laringotrakeobronkitis campak), sianosis sentral, atau distres napas akibat efusi pleura/edema paru (Kemenkes RI, 2020b; Tovar et al., 2024; WHO, 2016).
5. Ikon Otak / Kejang
Ensefalopati Dengue, Malaria Serebral, Meningoensefalitis, Tifoid Toksik
Penurunan kesadaran (letargi, iritabilitas, koma), kejang, paresis, atau kaku kuduk akibat sekuestrasi eritrosit terinfeksi P. falciparum di mikrovaskular serebral, edema serebri, atau perdarahan intrakranial (FEBRASGO, 2024; Kemenkes RI, 2019c, 2020b; WHO, 2023).
6. Ikon Lemas Ekstrem
Dehidrasi Berat / Syok Gastroenteritis Akut
Minimal 2 tanda dehidrasi berat WHO: letargi/tidak sadar, mata sangat cekung, tidak bisa/malas minum, dan turgor kulit perut kembali sangat lambat (≥2 detik) (American Academy of Family Physicians [AAFP], 2022; WHO, 2005).
7. Ikon Gigitan Hewan
Luka GHPR Kategori III & Ensefalitis Rabies
Luka gigitan transdermal tunggal/multipel berdarah dari anjing, kera, atau kucing liar (Kategori III WHO memerlukan pencucian luka 15 menit, VAR, dan SAR), atau gejala patognomonik hidrofobia, fotofobia, dan hipersalivasi otonom (Kemenkes RI, 2026; WHO, 2018).
8. Ikon Jantung Petir
Sindrom Koroner Akut / Code STEMI
Angina tipikal berupa rasa tertekan/berat di substernal menjalar ke lengan kiri, leher, rahang, atau punggung >20 menit disertai gejala otonom diaforesis (keringat dingin), mual, atau sinkop (European Society of Cardiology [ESC], 2023; Perhimpunan Dokter Spesialis Kardiovaskular Indonesia [PERKI], 2025).
9. Ikon Wajah Mencong
Code Stroke Akut (Iskemik / Hemoragik)
Defisit neurologis fokal mendadak mengacu pada akronim BE-FAST atau slogan Kemenkes SeGeRa Ke RS (Senyum tidak simetris/mencong, Gerak separuh tubuh melemah tiba-tiba, bicaRa pelo/afasia) (Kemenkes RI, 2019c, 2024).
10. Ikon Kepala Kilat
Krisis Hipertensi (Hipertensi Emergensi / Ensefalopati)
Kenaikan tekanan darah ekstrem disertai kerusakan organ target akut (Hypertension-Mediated Organ Damage / HMOD) seperti retinopati/papiledema (pandangan mendadak gelap/kabur), iskemia serebral, atau edema pulmonal akut (Kemenkes RI, 2021a; PERKI, 2025).
11. Ikon Pingsan / Buah
Krisis Hiperglikemia (KAD & SHH) / Hipoglikemia Berat
Penurunan kesadaran, agitasi, tremor dan pucat diaforetik (neuroglikopenia hipoglikemia), atau pernapasan cepat dan dalam (Kussmaul) disertai napas berbau buah/aseton akibat ketonemia pada Ketoasidosis Diabetik (Kemenkes RI, 2020a; PERKENI, 2021, 2024).

3.2 Pemetaan Ekologi One Health (Tahap 4 - Q4) dan Sistem Pakar Farmakovigilans Obat (Tahap 4 - Q5)
Pada Tahap 4 (Q4), sistem mengintegrasikan determinan spasio-ekologis sesuai mandat One Health dalam Permenkes Nomor 3 Tahun 2026 (Kemenkes RI, 2026). Indikator paling spesifik adalah penapisan riwayat beraktivitas/berenang di Danau Lindu, Lembah Napu, atau Lembah Bada (Sulawesi Tengah) untuk mendeteksi Skistosomiasis (Schistosoma japonicum). Di Indonesia, penyakit ini hanya endemik di 28 desa pada ketiga dataran tinggi tersebut (Kabupaten Sigi dan Kabupaten Poso), dengan 242 daerah fokus keong amfibi Oncomelania hupensis lindoensis seluas 1.407.225m2 (Dinas Kesehatan Provinsi Sulawesi Tengah & Kemenkes RI, 2024; Widjaja et al., 2017). Meskipun prevalensi pada manusia di Lembah Napu sempat ditekan hingga 0,15%, laju infeksi pada reservoar mamalia liar (tikus) masih mencapai 16% di Lindu dan 7,3%-22,7% di Napu, sehingga reinfeksi terus terjadi saat warga bertani atau mencuci di saluran air fokus keong (Satrija et al., 2017; WHO Indonesia, 2023). Selain itu, Q4 memetakan riwayat perjalanan 1-4 bulan dari Indonesia Timur (Papua, Maluku, NTT) atau area tambang/hutan untuk Malaria dan Frambusia (Kemenkes RI, 2017a, 2026), paparan banjir/lumpur tikus untuk Leptospirosis, hunian padat (asrama/pesantren) dan kontak serumah pasien OAT untuk TBC, Skabies, Tinea, dan Hepatitis A (Hengge et al., 2007; Kamath et al., 2024; Kemenkes RI, 2022a), serta faktor risiko PTM (riwayat keluarga lini pertama, merokok, sedentari, dan diet tinggi purin/lemak jenuh) (Perhimpunan Reumatologi Indonesia [IRA], 2024; PERKI, 2025).

Pada Tahap 4 (Q5), sistem menerapkan 5 Aturan Pemicu Farmakovigilans (Medication Safety Triggers) untuk melindungi lansia dan pasien komorbid di rumah:
Trigger 1A (Suspek DBD + Kontraindikasi Absolut NSAID): Jika pasien demam mengonsumsi Ibuprofen, Aspirin (ASA), Natrium Diklofenak, atau Asam Mefenamat, sistem memunculkan Pop-up Merah untuk menghentikan NSAID seketika dan menggantinya dengan Paracetamol serta kompres hangat, karena inhibisi COX-1 pada kondisi trombositopenia dan koagulopati dengue memicu perdarahan gastrointestinal masif, perforasi, dan Sindrom Reye (Alam et al., 2022; Mohiuddin, 2023; Sharp et al., 2021; U.S. Centers for Disease Control and Prevention [U.S. CDC], 2024; U.S. National Library of Medicine [U.S. NLM], 2024c).
Sub-Trigger 1B (Suspek DBD + Evaluasi Obat Komorbid PTM): Mengingat hanya 11,21% klinisi memahami penyesuaian obat komorbid saat dengue akut (Herman et al., 2021), jika pasien lansia PTM yang mengalami demam akut mengonsumsi Statin (Simvastatin/Atorvastatin), Diuretik (Furosemide/HCT), atau Antikoagulan (Warfarin), sistem memberikan Pop-up Peringatan Kritis untuk evaluasi penghentian sementara oleh dokter guna mencegah perburukan hepatopati/miositis dengue (elevasi SGOT/SGPT & CK), kolaps kardiovaskular saat fase plasma leakage, serta perdarahan saluran cerna sinergis (Tovar et al., 2024).
Trigger 2 (Suspek Diare Akut / Disentri + Larangan Antimotilitas): Jika pasien diare mengonsumsi Loperamide, Attapulgite, atau Kaolin-Pektin, sistem memunculkan Pop-up Kuning untuk menghentikan obat tersebut dan beralih ke Oralit dan Zinc, karena agonis opioid mu menghambat peristaltik propulsif usus yang pada infeksi invasif (Shigella, Salmonella, Entamoeba histolytica) memicu kolitis amebik fulminan, toxic megacolon, perforasi kolon, serta aritmia ventrikel (QTc prolongation) pada anak di bawah 2 tahun (Chansrichavala et al., 2015; Grobusch et al., 2025; Koo et al., 2007; Schiller et al., 2020; U.S. NLM, 2024b, 2024d).
Trigger 3 (Efek Samping Amlodipine vs. Filariasis Limfatik): Amlodipine memicu edema perifer pitting bilateral lebih tinggi dibanding non-DHP CCB (12,3% vs. 3,1%; risiko 2,8x lipat pada dosis tinggi) akibat vasodilatasi selektif arteriol pre-kapiler tanpa diimbangi venula post-kapiler, berbeda dari limfedema Filariasis yang asimetris, non-pitting (fibrosis/hiperkeratosis), dan menetap >3 bulan (Ahmed et al., 2024; Largeau et al., 2021; Liang et al., 2022; Moffatt et al., 2003; Putri et al., 2025; Sica, 2003; Zheng et al., 2026). Pop-up Biru mencegah rujukan palsu ke Poli NTD sekaligus mencegah prescribing cascade pemberian diuretik yang tidak perlu pada lansia, sembari menyarankan evaluasi kombinasi ACEi/ARB di FKTP yang menurunkan risiko edema sebesar 38% (RR 0,62) (Makani et al., 2011; Savage et al., 2020).
Trigger 4 (Efek Samping Captopril/ACEi vs. Tuberkulosis Paru): Inhibisi enzim ACE (kininase II) oleh Captopril/Lisinopril menyebabkan akumulasi bradikinin dan substansi P di saluran napas yang mengiritasi serat C tanpa mielin, menghasilkan batuk kering persisten non-produktif tanpa demam (Dicpinigaitis, 2014; U.S. NLM, 2024a). Pop-up Biru memverifikasi ada tidaknya gejala konstitusional TBC sesuai algoritma 5 Pertanyaan Skrining TBC Kemenkes sebelum menyimpulkan suspek TBC Paru (Kemenkes RI, 2023b).

3.3 Protokol Anamnesis Mendalam Dinamis (Tahap 5) pada 32 Entitas Penyakit
Pada Tahap 5, antarmuka web memunculkan pertanyaan History of Present Illness (HPI) secara spesifik berdasarkan klaster terpilih untuk membedakan 32 entitas penyakit secara presisi:

Klaster HPI (Tahap 5)
Cakupan 32 Entitas Penyakit
Karakteristik Klinis Patognomonik pada Algoritma & Sitasi Pedoman (APA 7)
Klaster 1: Demam Vektor & Zoonosis
1. DBD & Syok Dengue (DSS)

2. Malaria & Malaria Serebral

3. Chikungunya Akut & Kronis

4. Leptospirosis & Weil's Disease

5. Skistosomiasis (Katayama)
• DBD: Demam bifasik pelana kuda (saddleback) turun hari ke-3/4 disertai letargi & nyeri retro-orbital; deteksi fase kritis mencegah DSS dengan mortalitas <0,5% (Kemenkes RI, 2020b, 2021b; WHO, 2011).

• Malaria: Paroksisme periodik 2-3 hari (menggigil-demam-berkeringat) (WHO, 2023).

• Leptospirosis: Demam naik-turun + nyeri tekan hebat otot betis gastrocnemius (Kemenkes RI, 2022a).

• Chikungunya Kronis: Artralgia melumpuhkan skala VAS ≥7 durasi >90 hari (Barrera et al., 2023; Sharp et al., 2021).

• Skistosomiasis: Riwayat gatal swimmer's itch (dermatitis serkaria) diikuti demam Sindrom Katayama 4-8 minggu kemudian (Satrija et al., 2017; Widjaja et al., 2017).
Klaster 2: Saluran Napas & Dada
6. ISPA Akut

7. TBC Paru/Ekstraparu & Hemoptisis

8. Pneumonia Berat / Gagal Napas
• ISPA Akut: Batuk akut <14 hari disertai rinitis dan faringitis (Kemenkes RI, 2022a).

• TBC Paru: Algoritma 5 Pertanyaan: batuk produktif/kronis ≥14 hari disertai diaforesis nokturnal (keringat malam basah kuyup tanpa aktivitas), anoreksia, penurunan BB, demam subfebris, atau hemoptisis (Kemenkes RI, 2019d, 2023b).

• Pneumonia Berat: Sesak napas berat, retraksi dada bawah, stridor istirahat, sianosis (WHO, 2016).
Klaster 3: Pencernaan & Hepatobilier
9. Diare Akut & Dehidrasi Berat

10. Amebiasis / Disentri

11. Demam Tifoid & Tifoid Toksik

12. Hepatitis Akut A & B

13. Cacingan (STH)
• Diare Akut vs. Amebiasis: Diare cair >3x/hari tanpa darah/lendir vs. disentri darah/lendir disertai tenesmus perih (AAFP, 2022; Kemenkes RI, 2022a; Koo et al., 2007).

• Demam Tifoid: Pola demam step-ladder memuncak malam hari + nyeri tekan abdomen (Kemenkes RI, 2022a).

• Hepatitis Akut A/B: Bilirubinuria warna teh gelap + nyeri kuadran kanan atas (Kemenkes RI, 2022a).

• Cacingan (STH): Anak usia 1-12 tahun dengan malnutrisi kurus-perut buncit, pruritus ani nokturnal, atau ekspulsi cacing (Kemenkes RI, 2017b).
Klaster 4: Kulit, Lesi Mukosa & Eksantema
14. Skabies

15. Tinea (Dermatofitosis)

16. Kusta (PB & MB)

17. Frambusia (Yaws)

18. Campak (Ringan & Berat)

19. Varicella (Ringan & Berat)
• Skabies vs. Tinea: Pruritus nokturnal sela jari/lipatan vs. plak eritematosa bersisik tepi aktif central clearing gatal saat berkeringat (Hengge et al., 2007; Kemenkes RI, 2022a).

• Kusta: Tanda Kardinal Pertama berupa makula hipopigmentasi/eritematosa yang mengalami mati rasa (baal/anestesi) saat diuji tusuk jarum atau penebalan saraf tepi (Kemenkes RI, 2019a, 2019b).

• Frambusia: Papiloma/koreng bergranulasi mirip buah raspberry (mother yaw) akibat invasi Treponema pallidum subsp. pertenue melalui abrasi kulit (Kemenkes RI, 2017a, 2026).

• Campak vs. Varicella: Ruam makulopapular didahului prodromal 3C (cough, coryza, conjunctivitis) vs. vesikel menyebar sentrifugal (Kemenkes RI, 2022a).
Klaster 5: Pembengkakan NTD
20. Filariasis Limfatik
• Filariasis Limfatik: Edema ekstremitas bawah kronis >3 bulan, bersifat asimetris, menetap, dan tidak mencekung saat ditekan jari (non-pitting edema) (Kemenkes RI, 2014, 2026; Moffatt et al., 2003).
Klaster 6: Gula & Saraf PTM
21. DM Tipe 2 Stabil/Katabolik

22. Krisis KAD/SHH & Hipoglikemia

23. Neuropati, Ulkus & Acanthosis
• DM Tipe 2 & Polineuropati: Trias klasik 3P (Poliuria, Polidipsia, Polifagia) disertai penurunan BB katabolik tanpa sebab jelas; parestesia/kebas bilateral simetris berpola kaos kaki (stocking-and-glove distribution) (Kemenkes RI, 2020a; PERKENI, 2021, 2024).
Klaster 7: Tekanan, Kepala & Vaskular PTM
24. Hipertensi Derajat 1 & 2

25. Krisis Hipertensi Emergensi

26. Angina Pektoris Stabil & STEMI

27. Dislipidemia

28. Stroke Akut
• Hipertensi & Angina Pektoris Stabil: Sakit kepala oksipital dan tengkuk berat/kaku; nyeri dada substernal atau sesak napas yang dipicu eksklusif oleh aktivitas fisik (naik tangga) dan mereda dengan istirahat (Perhimpunan Dokter Hipertensi Indonesia [InaSH], 2019; Kemenkes RI, 2021a; PERKI, 2025).
Klaster 8: Sendi PTM & Kegawatan Lain
29. Artritis Gout Akut & Tofus

30. Mialgia Ringan

(+31. Rabies & 32. Meningoensefalitis di Q3)
• Artritis Gout Akut: Serangan inflamasi sendi monoartikular mendadak pada sendi metatarsofalangeal pertama (jempol kaki / Podagra) dengan bengkak, eritema, teraba panas, dan nyeri tekan ekstrem yang mencapai puncak dalam <12-24 jam (IRA, 2024).


3.4 Objektivikasi Klinis Mandiri, Kalibrasi Fitzpatrick IV-VI & Skor Risiko CVD WHO SEAR-B (Tahap 6-7)
Untuk mengatasi kesenjangan kepemilikan instrumen diagnostik rumah tangga pada Laporan SKI 2023, Tahap 6 dan logika klinis Tahap 7 menjalankan tiga mekanisme objektivikasi mandiri di peramban web:
Proksi Hemodinamik (Q6) & Proksi Antropometri (Q7): Apabila pengguna tidak memiliki termometer, tensimeter, timbangan, atau pita meteran, sistem menyediakan opsi proksi fisik: (a) menggigil gemetar hebat (rigors) atau keringat basah kuyup sebagai proksi kurva demam tinggi, dan perabaan denyut nadi radialis cepat/kuat saat istirahat sebagai proksi takikardia; (b) pakaian atau celana menjadi sangat longgar dalam 1-2 bulan terakhir sebagai proksi hiperkatabolisme (IMT <18,5 kg/m²) yang meningkatkan probabilitas posterior TBC Paru, Cacingan STH, dan DM tipe 2 dekompensata; serta (c) celana terasa makin sempit di pinggang sebagai proksi obesitas sentral (mengacu pada rentang IMT normal dewasa Indonesia 18,5-22,9 kg/m² dan batas lingkar pinggang obesitas sentral ≥90 cm pada laki-laki serta ≥80 cm pada perempuan sesuai Kepmenkes 4634/2021 dan PERKENI 2024) yang menjadi prediktor sindrom metabolik dan keparahan klinis malaria P. falciparum (Kemenkes RI, 2021a, 2024; PERKENI, 2024).
Kalibrasi Klinis Citra Kulit Fitzpatrick IV-VI, Sklera Mata & Rule-Based Multimodal Override (Q8): Pengambilan citra lesi kulit melalui kamera web ponsel (ruam DBD/Campak, vesikel Varicella, bercak Kusta, borok Frambusia/Ulkus Diabetikum, Tofus Gout, dan Acanthosis Nigricans) dikalibrasi khusus untuk kulit sawo matang hingga gelap (Fitzpatrick IV-VI). Studi perintis pada 1.709 citra klinis pasien berkulit gelap dan uji lapangan aplikasi WHO Skin NTDs membuktikan sensitivitas klinis ~80%-88% pada NTD kulit dengan penyaringan uncertainty score 0,200 (WHO, 2022; Yotsu et al., 2023a, 2023b, 2025), sedangkan pemisahan piksel latar belakang pada dataset Fitzpatrick 17k mendongkrak akurasi tugas baru sebesar 43,3% dan memangkas ketimpangan Gini warna kulit sebesar 20,9% (Zhang et al., 2024). Namun, karena evaluasi independen membuktikan sensitivitas visual AI turun dari 87,2% pada kusta klasik menjadi 69,6% pada kusta reaksional/atipikal (Deps et al., 2025a, 2025b), sistem menerapkan Rule-Based Multimodal Override: hasil uji mandiri tusuk jarum yang positif mati rasa (baal) atau nyeri saraf tepi pada Tahap 5 wajib mengunci Rute Kuning Khusus meskipun skor kepercayaan kamera rendah. Untuk mata kuning (ikterus Hepatitis A/B) vs. conjunctival suffusion (Leptospirosis), pencitraan didasarkan pada kromatisitas sklera ambient-subtracted tanpa kartu kalibrasi warna eksternal (Outlaw et al., 2020; Wang et al., 2021, 2023).
WHO Non-Laboratory-Based CVD Risk Chart (SEAR-B) & Vital Sign Override (Tahap 7): Selaras dengan Pedoman Puskesmas Klaster 3 Kemenkes RI dan Kepmenkes 1186/2022, estimasi risiko 10 tahun kejadian kardiovaskular fatal/non-fatal (infark miokard/stroke) dihitung menggunakan WHO Non-Laboratory-Based CVD Risk Chart wilayah epidemiologi SEAR-B (Indonesia) berbasis 5 variabel tanpa tes darah: Usia (40-74 tahun), Jenis Kelamin, Status Merokok, Tekanan Darah Sistolik, dan IMT ke dalam 5 pita risiko (<5% Rute Hijau, 5%-<10%, 10%-<20%, 20%-<30%, dan ≥30%) (Gujarathi et al., 2025; Kemenkes RI, 2022a, 2024; Khanal et al., 2023; Rezaei et al., 2023). Dilengkapi aturan Cross-Validation Override: jika Suhu ≥39,5 °C (hiperpireksia) atau Tekanan Darah Sistolik ≥160 mmHg (ambang Hipertensi Derajat 2 yang mewajibkan inisiasi farmakoterapi antihipertensi segera oleh dokter FKTP dan skrining HMOD sesuai Pedoman PERKI 2025 dan Kepmenkes 4634/2021), sistem otomatis membatalkan Rute Hijau dan menaikkan prioritas ke Rute Kuning (Kemenkes RI, 2021a; PERKI, 2025).
BAB IV ARSITEKTUR SISTEM WEB, PEMODELAN KECERDASAN BUATAN & REKAYASA PERANGKAT LUNAK (TAHAP 7)

4.1 Arsitektur Ekosistem Web Progresif (PWA), Dual-Sided Web Dashboard, dan Tech Stack Keseluruhan

4.2 Pemodelan Machine Learning untuk Imputasi Proksi Antropometri dan Klasifikasi Gejala Tabular

4.3 Arsitektur Computer Vision Terkalibrasi Fitzpatrick IV-VI, Segmentasi Piksel Latar Belakang, dan Kromatisitas Sklera Digital

4.4 Rekayasa Rule Engine Deterministik, Multimodal Override, dan Inferensi Lokal di Peramban (In-Browser Client-Side Inference)

4.5 Keamanan Siber Web, Enkripsi Data Lokal (Privacy-by-Design), dan Pengujian Performa Sistem

























BAB V ORKESTRASI RUJUKAN BERJENJANG, SPGDT PSC 119 & INTEROPERABILITAS SATUSEHAT HL7 FHIR R4 (TAHAP 8-9)

5.1 Protokol Klinis dan Logistik pada Empat Rute Triase Berjenjang (Tahap 8)
Luaran triase pada Tahap 8 menerjemahkan matriks kompetensi SKDI dalam Kepmenkes 1186/2022 dan Permenkes Nomor 3 Tahun 2026 ke dalam empat rute operasional pada layar web pengguna dan dasbor web faskes (Kemenkes RI, 2022a, 2026):

Rute Triase (Tahap 8)
Spektrum Diagnosis (Infeksi, NTD, & PTM)
Tindakan Sistem Web, Logistik Obat & Pemeriksaan Penunjang
Protokol Pertolongan Pertama, Edukasi & Target Waktu Klinis
1. RUTE HIJAU

(Perawatan Mandiri / Apotek / Telemedisin)
ISPA Ringan, Diare Akut tanpa dehidrasi, Skabies, Tinea, Varicella Ringan, STH Ringan, Risiko PTM Rendah (Skor CVD SEAR-B <5%), Mialgia Ringan.
Navigasi peta web GPS ke Apotek untuk obat bebas/bebas terbatas (Oralit, Zinc, Paracetamol, Krim Miconazole) serta Krim Permethrin 5% melalui Apoteker (skema DOWA) atau e-resep telemedisin Mobile JKN; larangan mutlak rekomendasi antibiotik tanpa resep (Kemenkes RI, 2021c); tombol integrasi Mobile JKN.
Ventilasi jendela pagi hari & etika batuk (ISPA/TBC); dekontaminasi pakaian/selimut dengan air panas >60 °C (Skabies) (Hengge et al., 2007); pembatasan garam ≤1 sdt/hari, gula <4 sdm/hari, dan olahraga 150 menit/minggu (30-60 menit/hari, 3-5 hari/minggu) (Kemenkes RI, 2021a; PERKI, 2025).
2. RUTE KUNING

(FKTP Puskesmas / Klinik Pratama)
Infeksi: DBD fase demam biasa, Malaria tanpa komplikasi, Chikungunya akut, Demam Tifoid, Hepatitis A/B, Amebiasis, Leptospirosis dini, Varicella berat.

PTM: DM Tipe 2 Stabil, Hipertensi Derajat 1-2, Artritis Gout, Dislipidemia, Neuropati Diabetik.
Penerbitan QR Code Rujukan FKTP & integrasi tombol "Buat Janji / Daftar Poli" Mobile JKN; Pop-up Mandat Wajib Puasa 10-12 Jam (hanya minum air putih) malam hari sebelum pemeriksaan lab PTM (GDP, GD 2 Jam PP, Profil Lipid, Asam Urat, Ureum/Kreatinin, HbA1c) guna mencegah elevasi trigliserida kilomikron post-prandial dan pembatalan periksa darah lansia (PERKENI, 2024; PERKI & PERKENI, 2022), atau lab Infeksi (Darah Rutin serial, NS1, Apusan Darah, Tubex/Widal, Feses).
Pada Gout Akut: Kompres es lokal, larangan keras memijat sendi bengkak (karena manipulasi mekanis memobilisasi pelepasan kristal monosodium urate / MSU ke cairan sinovial dan memperhebat badai sitokin IL-1), serta hidrasi air putih >2 liter/hari (8-16 gelas/hari) guna mencegah urolitiasis asam urat (IRA, 2024).

Pada DBD: Hidrasi cairan isotonik/oralit 2-3 liter/hari & pantau warning signs (Kemenkes RI, 2020b).
3. RUTE KUNING KHUSUS

(Poli Program Nasional Kemenkes)
Tuberkulosis (TBC Paru/Ekstraparu), Kusta (PB/MB), Frambusia, Filariasis Limfatik, Skistosomiasis, Campak Ringan tanpa komplikasi.
Navigasi eksklusif ke Puskesmas penyelenggara Poli DOTS & Eradikasi NTD; Web Pre-Notification otomatis kesiapan Ruang Isolasi Infeksi Airborne (khusus TBC & Campak untuk cegah infeksi nosokomial di ruang tunggu) serta jaminan stok logistik OAT, Blister MDT Kusta (PB 6 blister dalam 6-9 bulan / MB 12 blister dalam 12-18 bulan), Azitromisin POPM Frambusia, dan 3 pot tinja metode Kato-Katz / Praziquantel (Badan Kebijakan Pembangunan Kesehatan [BKPK] Kemenkes RI, 2023; Kemenkes RI, 2017a, 2019a, 2019b, 2026).
Penggunaan masker bedah bagi suspek TBC/Campak sejak dari rumah untuk memutus rantai transmisi droplet/airborne; penapisan kontak serumah untuk pemberian kemoprofilaksis Rifampisin dosis tunggal pada Kusta (Kemenkes RI, 2019b) atau POPM Azitromisin sekampung halaman pada temuan kasus Frambusia disertai surveilans serologis 3 tahun (Kemenkes RI, 2017a).
4. RUTE MERAH

(IGD FKRTL & SPGDT PSC 119)
Infeksi: Syok Dengue (DSS), Malaria Serebral, AKI Leptospirosis, Pneumonia/Campak Berat dengan stridor, Ensefalitis Rabies, TBC Hemoptisis Masif.

PTM: STEMI, Stroke Akut, Krisis Hipertensi/Ensefalopati, Koma Diabetik (KAD/SHH/Hipoglikemia Berat).
Aktivasi sirene visual/audio di peramban web & tombol [Panggil Ambulans (119)] terhubung ke NCC / PSC 119; transmisi otomatis Pre-Arrival Tele-triage Data & koordinat GPS ke dasbor web SIMRS IGD rujukan; Live Tracking ambulans (Kemenkes RI, 2016).
Target Waktu Kritis: Door-to-Balloon / EKG <10 menit (STEMI); Door-to-Needle <30 menit dalam Golden Hour <4,5 jam (Trombolisis Stroke); Resusitasi Cairan <15 menit (DSS); penurunan MAP 25% pada 1 jam pertama (Krisis Hipertensi) (Kemenkes RI, 2019c, 2020b; PERKI, 2025).


5.2 Prosedur Aktivasi Darurat SPGDT PSC 119 dan Protokol Pertolongan Pertama (First Aid) Presisi
Integrasi tombol darurat [Panggil Ambulans (119)] dan pengiriman telemetri pra-fasilitas pada Rute Merah merupakan implementasi langsung dari Peraturan Menteri Kesehatan Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT) Pasal 5 ayat (3) dan Pasal 27 ayat (3) huruf b untuk mempercepat response time penanganan pra-fasilitas (Kemenkes RI, 2016). Sambil menunggu ambulans tiba melalui layar Live Tracking di peramban web, sistem memandu keluarga/pendamping pasien dengan instruksi visual Bantuan Hidup Dasar (BHD) yang telah dikalibrasi secara klinis:
Luka Gigitan Hewan Penular Rabies (GHPR): Mencuci luka gigitan dengan sabun di bawah air mengalir selama 15 menit tanpa henti sebelum diberangkatkan untuk mendapatkan Vaksin Anti Rabies (VAR) dan Serum Anti Rabies (SAR) (WHO, 2018).
Penurunan Kesadaran, Stroke Akut & Syok Dengue: Menerapkan larangan mutlak pemberian makanan atau minuman per oral (Nil Per Os / NPO) saat kesadaran menurun guna mencegah aspirasi paru. Pada pasien Stroke Akut dengan penurunan kesadaran, pasien diposisikan dalam posisi pemulihan miring (lateral recovery position) untuk menjaga patensi jalan napas (sedangkan elevasi kepala 30 derajat dikhususkan bagi pasien dengan peningkatan tekanan intrakranial yang jalan napasnya telah aman) (Kemenkes RI, 2019c). Pada pasien Syok Dengue (DSS), tindakan peninggian kaki (passive leg raising) hanya boleh dilakukan apabila pasien tidak mengalami sesak napas akibat efusi pleura masif atau edema paru akut (Kemenkes RI, 2020b; Tovar et al., 2024).

5.3 Standar Interoperabilitas RME SATUSEHAT HL7 FHIR R4 dan Mobile JKN (Tahap 9)
Untuk memangkas administrasi manual dan antrian di Puskesmas sesuai Permenkes Nomor 24 Tahun 2022 tentang Rekam Medis (masa retensi minimal 25 tahun) dan Pedoman Tata Kelola Rumah Sakit Bidang Operasional Kemenkes RI (Kemenkes RI, 2022b; Kemenkes RI & Dinas Kesehatan Provinsi Kalimantan Tengah, 2025), fitur pemindaian QR Code Handover pada Web Scanner Dashboard Puskesmas langsung menginjeksi data triase ke dalam SIMPUS/SIMRS menggunakan standar HL7 FHIR Release 4 (R4) SATUSEHAT tanpa entri ulang (zero-retyping):

Komponen Data pada QR Code Web
HL7 FHIR R4 Resource Standar SATUSEHAT
Sistem Kode / Terminologi Wajib Kemenkes RI
Implementasi Spesifik pada Dasbor Web RME Puskesmas / SIMRS
Identitas & Demografi Pasien (Tahap 1)
Patient & Encounter
NIK / IHS Number SATUSEHAT
Memetakan usia, jenis kelamin administratif (male/female), dan mengaitkan sesi triase mandiri dengan kunjungan fasyankes melalui Encounter.
Tanda Vital, Antropometri & Skor CVD (Tahap 6-7)
Observation (vital-signs & exam)
LOINC & UCUM (Satuan Ukur)
Mengkodekan Suhu tubuh (8310-5 dalam Cel), TD Sistolik (8480-6), TD Diastolik (8462-4), Tinggi Badan (8302-2), Berat Badan (29463-7), IMT (39156-5), Lingkar Pinggang (8280-0), serta Status Kehamilan (82810-3).
Keluhan Utama, HPI & Suspek Diagnosis (Tahap 2, 5, 8)
Condition (provisional / differential)
ICD-10 (Klaim JKN) & SNOMED-CT (Klinis)
Mengkodekan suspek penyakit ke ICD-10: J06 (ISPA akut), A91 (DBD), A15 (TBC Paru), A30 (Kusta), A66 (Frambusia), B65.2 (S. japonicum), E11 (DM Tipe 2), I10 (Hipertensi), M10 (Gout).
Riwayat Obat Rutin & Peringatan Interaksi (Tahap 4 - Q5)
MedicationStatement & DetectedIssue
KFA (Kamus Farmasi & Alat Kesehatan Kemenkes RI)
Mencatat konsumsi NSAID, Loperamide, Amlodipine, Captopril, Statin, Diuretik, atau Warfarin dengan kode presisi KFA agar RME dokter dan apoteker FKTP langsung menerima flag interaksi obat secara otomatis.
Rekomendasi Pemeriksaan Laboratorium (Tahap 8)
ServiceRequest (Laboratory procedure)
LOINC & SNOMED-CT
Mengirimkan draf pengantar pesanan lab (Darah Rutin, NS1, GDP, Profil Lipid, Asam Urat, Kreatinin, TCM TBC, Kato-Katz) beserta atribut patientInstruction berisi mandat puasa 10-12 jam.
Pendaftaran antrian Online & Rujukan (Tahap 8-9)
Appointment & ServiceRequest
API Web Service BPJS Kesehatan (Mobile JKN / PCare)
Menghubungkan tombol "Buat Janji / Daftar Poli" ke endpoint antrian FKTP terdaftar milik peserta JKN untuk memangkas hambatan administratif di Puskesmas.


5.4 Kepatuhan Mediko-Legal dan Perlindungan Data Pribadi
Selaras dengan Undang-Undang Nomor 17 Tahun 2023 tentang Kesehatan dan Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (Pemerintah Republik Indonesia, 2022, 2023), pemrosesan citra klinis sensitif (seperti foto lesi kusta, frambusia, atau skabies pada Q8) dijalankan di memori peramban lokal perangkat pengguna tanpa diunggah ke peladen awan pihak ketiga, sedangkan transmisi data ke SATUSEHAT, Mobile JKN, atau PSC 119 hanya dieksekusi berdasarkan persetujuan sah (explicit informed consent) pasien atau dalam kondisi darurat penyelamatan nyawa pada Rute Merah. Layar hasil wajib menampilkan penafian mediko-legal bahwa luaran aplikasi web adalah alat bantu triase awal (Clinical Decision Support / Triage Tool) dan bukan diagnosis medis final maupun pengganti pemeriksaan fisik dan laboratorium oleh dokter.






BAB VI DAMPAK SISTEMIK, KEBERLANJUTAN & PETA JALAN IMPLEMENTASI

6.1 Matriks Dampak Terukur (Key Performance Indicators) terhadap Subtema Healthcare

Permasalahan pada Subtema Healthcare
Solusi Spesifik pada GardaMedika-Web
Target Indikator Kinerja Utama (KPI)
1. Puskesmas dan klinik kewalahan menghadapi antrian panjang, administrasi manual, serta pengelolaan data pasien yang belum optimal.
• Penyaringan kasus ringan (SKDI 4A) ke Rute Hijau.

• Pop-up wajib puasa 10-12 jam di Rute Kuning.

• One-click booking Mobile JKN & pindaian QR Code pada Web Scanner Dashboard Puskesmas berstandar SATUSEHAT HL7 FHIR R4.
• Penurunan beban antrian kasus ringan di FKTP >30%.

• 0% pembatalan cek lab lansia/PTM akibat lupa berpuasa.

• Pemangkasan waktu anamnesis & entri manual RME >50% (zero-retyping).
2. Masyarakat di wilayah kepulauan dan pedalaman terkendala jarak dan biaya transportasi untuk menjangkau tenaga medis dan layanan kesehatan.
• Arsitektur Web PWA Zero-Install & Offline-Capable yang berjalan ringan tanpa sinyal internet stabil.

• Pemetaan spasio-ekologis One Health & deteksi NTD kulit Fitzpatrick IV-VI.

• Web Pre-Notification kesiapan stok obat (MDT, OAT, Praziquantel) di Rute Kuning Khusus.
• 100% ketersediaan fungsi triase di area blank-spot tanpa makan memori ponsel.

• Penghematan biaya transportasi warga pedalaman dengan mencegah perjalanan sia-sia ke faskes yang kosong logistik obat NTD/DOTS.
3. Usia produktif berisiko diabetes/hipertensi/penyakit kronis lain tetapi jarang memeriksakan diri, sehingga membutuhkan pemantauan dini yang mudah dijangkau.
• Akses skrining instan 1 klik via tautan peramban web.

• Imputasi proksi fisik (celana menyempit / baju melonggar) untuk mengatasi ketiadaan alat ukur (data SKI 2023).

• Kalkulasi risiko 10 tahun WHO Non-Laboratory CVD Risk Chart (SEAR-B).
• Menjangkau 35%-80% populasi dewasa yang belum memiliki alat ukur medis di rumah.

• Skrining dini PTM tuntas dalam <3 menit dari rumah tanpa instalasi aplikasi dan tanpa sampel darah.
4. Keluarga yang merawat lansia kesulitan memantau kondisi kesehatan, kepatuhan pengobatan, dan menjangkau bantuan sehari-hari.
• 5 Trigger Farmakovigilans Obat (Q5) untuk memantau efek samping & interaksi obat rutin lansia.

• Deteksi 11 Red Flags, tombol darurat PSC 119, Live Tracking, dan panduan visual BHD langsung di peramban.
• 0 kasus perdarahan iatrogenik NSAID-DBD & eliminasi prescribing cascade Amlodipine.

• Pencapaian target Door-to-Balloon <10 menit, Door-to-Needle <30 menit, dan resusitasi syok <15 menit.


6.2 Strategi Implementasi Ekosistem Nasional & Keberlanjutan (Sustainability)
Pengujian Regulatory Sandbox DTO Kemenkes RI: Memanfaatkan kerangka UU Nomor 17 Tahun 2023 untuk menguji keamanan klinis, audit keadilan algoritma lintas warna kulit Fitzpatrick, dan sertifikasi standar HL7 FHIR R4 SATUSEHAT (Pemerintah Republik Indonesia, 2023).
Integrasi B2G (Business-to-Government) pada Ekosistem Web Puskesmas Klaster 3 & Mobile JKN: Karena berbasis web standar terbuka, sistem ini dapat langsung disematkan (embedded webview / direct link) ke dalam ekosistem BPJS Kesehatan serta dibuka langsung di komputer seluruh Puskesmas di Indonesia tanpa biaya pengadaan perangkat keras baru.
Efisiensi Biaya Komputasi (Near-Zero Cloud Inference Cost): Pemrosesan inferensi di peramban perangkat pengguna (client-side) menekan biaya operasional peladen pusat (cloud server) hingga >85%, memastikan keberlanjutan finansial jangka panjang.
6.3 Peta Jalan Pengembangan (Development Roadmap)
Fase 1 - Hackathon Web MVP & Validasi In-Silico (Bulan 1-3): Pembangunan antarmuka Patient Self-Triage Web (PWA) 9 Tahap dan FKTP Web Scanner Dashboard, integrasi mesin aturan 11 Red Flags (Q3) dan 5 Trigger Farmakovigilans (Q5), pemodelan machine learning & computer vision (Bab IV), serta generator/pemindai QR Code JSON HL7 FHIR R4.
Fase 2 - Regulatory Sandbox & Uji Validasi Klinis Prospektif (Bulan 4-6): Uji konkordansi hasil triase sistem web terhadap diagnosis dokter FKTP di Puskesmas perkotaan serta Puskesmas daerah endemis NTD (Sulawesi Tengah dan Indonesia Timur).
Fase 3 - Integrasi Ekosistem Nasional (Bulan 7-12): Koneksi endpoint produksi API SATUSEHAT Kemenkes RI, Web Service antrian Online Mobile JKN / PCare BPJS Kesehatan, dan sistem dispatch NCC / PSC 119 Kabupaten/Kota.



























DAFTAR PUSTAKA

Ahmed, S., et al. (2024). Case report: Escitalopram-associated lower limb edema and differential diagnosis of drug-associated lower limb edema. Frontiers in Psychiatry, 15, Article 1394813. https://doi.org/10.3389/fpsyt.2024.1394813
Alam, S. M., Qasswal, M., Ahsan, M. J., Walters, R. W., & Chandra, S. (2022). Selective serotonin reuptake inhibitors increase risk of upper gastrointestinal bleeding when used with NSAIDs: A systemic review and meta-analysis. Scientific Reports, 12(1), Article 14452. https://doi.org/10.1038/s41598-022-18654-2
American Academy of Family Physicians. (2022). Acute diarrhea in adults: Evaluation and management clinical guideline. American Family Physician, 106(1), 72-80. https://www.aafp.org/afp/2022/0700/acute-diarrhea
Badan Kebijakan Pembangunan Kesehatan Kementerian Kesehatan Republik Indonesia. (2023). Pedoman pengendalian schistosomiasis dan pemeriksaan laboratorium metode Kato-Katz. Kementerian Kesehatan Republik Indonesia.
Barrera, R., et al. (2023). Dengue, chikungunya and Zika arbovirus infections in Caribbean and tropical regions (PMCID: PMC10090388). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC10090388/
Chansrichavala, P., et al. (2015). Loperamide therapy for voluminous diarrhea in infectious disease settings (PMCID: PMC4366607). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC4366607/
Deps, P., Amorim, B. B. C., Repsold, T., & Almonfrey, D. (2025a). Independent assessment of the World Health Organization Skin Neglected Tropical Diseases application for leprosy detection (PMID: 42006576; PMCID: PMC13086047). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC13086047/
Deps, P., et al. (2025b). Artificial intelligence and integrated management of skin-related neglected tropical diseases. British Journal of Dermatology, 193(Suppl. 1), Article ljaf212. https://doi.org/10.1093/bjd/ljaf212
Dicpinigaitis, P. V. (2014). ACE inhibitors: Upper respiratory symptoms, bradykinin accumulation, and differential diagnosis. BMJ Case Reports, 2014, Article bcr2014205462. https://doi.org/10.1136/bcr-2014-205462
Dinas Kesehatan Provinsi Sulawesi Tengah & Kementerian Kesehatan Republik Indonesia. (2024). Schistosomiasis di Sulawesi Tengah: Epidemiologi, penularan, dan intervensi 2019-2024. Dinas Kesehatan Provinsi Sulawesi Tengah. https://dinkes.sultengprov.go.id/schistosomiasis-di-sulawesi-tengah-epidemiologi-penularan-dan-intervensi-2019-2024/
European Society of Cardiology. (2023). 2023 ESC Guidelines for the management of acute coronary syndromes. European Heart Journal, 44(38), 3720-3826. https://doi.org/10.1093/eurheartj/ehad191
Federação Brasileira das Associações de Ginecologia e Obstetrícia. (2024). Prevention, diagnosis, and treatment protocol of dengue during pregnancy and the postpartum period. Revista Brasileira de Ginecologia e Obstetrícia, 46, Article e-rbgo73. https://doi.org/10.61622/rbgo/2024rbgo73
Grobusch, M. P., et al. (2025). Racecadotril versus loperamide for acute diarrhea of infectious origin (PMCID: PMC12098968). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC12098968/
Gujarathi, A. P., Powar, J., Patil, R., Padhyegurjar, S., Ghodake, A. K., & Shaikh, M. H. M. A. (2025). Estimation of cardiovascular risk by using WHO/ISH charts and Correlation & Regression Tree (CART) analysis in adults of rural North Maharashtra, India. National Journal of Community Medicine, 16(11), 1101-1108. https://doi.org/10.55489/njcm.161120255801
Hengge, U. R., Currie, B. J., Jäger, G., Lupi, O., & Schwartz, R. A. (2007). Scabies: A ubiquitous neglected skin disease. Trends in Parasitology, 23(10), 485-493. https://doi.org/10.1016/j.pt.2007.08.007
Herman, L., et al. (2021). Assessment of knowledge, attitudes, and practices regarding dengue and NSAID contraindications among healthcare practitioners (PMCID: PMC8389296). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC8389296/
Ikatan Dokter Anak Indonesia. (2022). Pedoman nasional pelayanan kedokteran & konsensus tata laksana infeksi dengue anak dan remaja. Badan Penerbit Ikatan Dokter Anak Indonesia. https://www.idai.or.id/professional-resources/pedoman-konsensus/pedoman-nasional-pelayanan-kedokteran-tata-laksana-infeksi-dengue-anak-dan-remaja
Jones, O. T., Matin, R. N., van der Schaar, M., Prathivadi Bhayankaram, K., Ranmuthu, C. K. I., Islam, M. S., Behiyat, D., Boscott, R., Calanzani, N., Emery, J., Williams, H. C., & Walter, F. M. (2022). Artificial intelligence and machine learning algorithms for early detection of skin cancer in community and primary care settings: A systematic review. The Lancet Digital Health, 4(6), e466-e476. https://doi.org/10.1016/S2589-7500(22)00023-1
Kamath, S., et al. (2024). Using artificial intelligence on dermatology conditions in Uganda: Epidemiology and burden of tropical skin diseases (PMCID: PMC10782289). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC10782289/
Kementerian Kesehatan Republik Indonesia. (2014). Peraturan Menteri Kesehatan Republik Indonesia Nomor 94 Tahun 2014 tentang Penanggulangan Filariasis (Berita Negara Republik Indonesia Tahun 2014 Nomor 2036). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2016). Peraturan Menteri Kesehatan Republik Indonesia Nomor 19 Tahun 2016 tentang Sistem Penanggulangan Gawat Darurat Terpadu (SPGDT). Direktorat Pelayanan Kesehatan Rujukan Kementerian Kesehatan Republik Indonesia. https://keslan.kemkes.go.id/lakip_files/direktorat_pelayanan_kesehatan_rujukan_rak_2021.pdf
Kementerian Kesehatan Republik Indonesia. (2017a). Peraturan Menteri Kesehatan Republik Indonesia Nomor 8 Tahun 2017 tentang Eradikasi Frambusia (Berita Negara Republik Indonesia Tahun 2017 Nomor 351). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/111971/permenkes-no-8-tahun-2017
Kementerian Kesehatan Republik Indonesia. (2017b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 15 Tahun 2017 tentang Penanggulangan Cacingan (Berita Negara Republik Indonesia Tahun 2017 Nomor 438). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2019a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/308/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tatalaksana Kusta. Kementerian Kesehatan Republik Indonesia. https://ayosehat.kemkes.go.id/topik-penyakit/pencegahan-infeksi-pada-usia-produktif/kusta
Kementerian Kesehatan Republik Indonesia. (2019b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 11 Tahun 2019 tentang Penanggulangan Kusta (Berita Negara Republik Indonesia Tahun 2019 Nomor 449). Kementerian Kesehatan Republik Indonesia. https://peraturan.bpk.go.id/Details/138606/permenkes-no-11-tahun-2019
Kementerian Kesehatan Republik Indonesia. (2019c). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/394/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Stroke (beserta Pedoman PERDOSSI). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2019d). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/755/2019 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Tuberkulosis (beserta Pedoman PDPI). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2020a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/603/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Diabetes Melitus Tipe 2 Dewasa. Kementerian Kesehatan Republik Indonesia. https://rsudhaulussymaluku.com/unduh/4
Kementerian Kesehatan Republik Indonesia. (2020b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/9845/2020 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue pada Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.kemkes.go.id/eng/pnpk-2020---tata-laksana-infeksi-dengue-pada-dewasa
Kementerian Kesehatan Republik Indonesia. (2021a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4634/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Hipertensi Dewasa. Kementerian Kesehatan Republik Indonesia. https://www.prescribingcompanion.com/indonesia/kondisi-klinis-umum-lainnya/f-kardiovaskular/6-hipertensi-esensial/
Kementerian Kesehatan Republik Indonesia. (2021b). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/4636/2021 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Infeksi Dengue Anak dan Remaja. Kementerian Kesehatan Republik Indonesia. http://www.kemkes.go.id/id/pnpk-2021---infeksi-dengue-anak-dan-remaja
Kementerian Kesehatan Republik Indonesia. (2021c). Peraturan Menteri Kesehatan Republik Indonesia Nomor 28 Tahun 2021 tentang Pedoman Penggunaan Antibiotik (Berita Negara Republik Indonesia Tahun 2021 Nomor 1076). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2022a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1186/2022 tentang Panduan Praktik Klinis bagi Dokter di Fasilitas Pelayanan Kesehatan Tingkat Pertama (FKTP). Kementerian Kesehatan Republik Indonesia. https://manuver.tireg7.net/wp-content/uploads/2025/01/KEPMENKES-HK-01-07-MENKES-1186-2022-2.pdf
Kementerian Kesehatan Republik Indonesia. (2022b). Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis (Berita Negara Republik Indonesia Tahun 2022 Nomor 829). Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2023a). Keputusan Menteri Kesehatan Republik Indonesia Nomor HK.01.07/MENKES/1634/2023 tentang Pedoman Nasional Pelayanan Kedokteran (PNPK) Tata Laksana Penyakit Ginjal Kronik. Kementerian Kesehatan Republik Indonesia.
Kementerian Kesehatan Republik Indonesia. (2023b). Petunjuk teknis kolaborasi TBC-HIV. Direktorat Jenderal Pencegahan dan Pengendalian Penyakit Kementerian Kesehatan Republik Indonesia. https://kemkes.go.id/
Kementerian Kesehatan Republik Indonesia. (2024). Pedoman kerja Puskesmas klaster 3: Kesehatan usia dewasa dan lanjut usia (Memuat statistik Survei Kesehatan Indonesia / SKI 2023 dan tabel prediksi risiko PTM adaptasi WHO Cardiovascular Disease Risk Charts). Kementerian Kesehatan Republik Indonesia. https://renbut.kemkes.go.id/regulasi/Pedoman%20Puskesmas%20Klaster%203.pdf
Kementerian Kesehatan Republik Indonesia & Dinas Kesehatan Provinsi Kalimantan Tengah. (2025). Pedoman tata kelola rumah sakit: Buku 4 bidang operasional (Standar interoperabilitas SATUSEHAT HL7 FHIR R4 dan pengkodean LOINC). Kementerian Kesehatan Republik Indonesia. https://dinkes.kalteng.go.id/wp-content/uploads/2025/10/Pedoman-Tata-Kelola-Rumah-Sakit-Buku-4-Bidang-Operasional.pdf
Kementerian Kesehatan Republik Indonesia. (2026). Peraturan Menteri Kesehatan Republik Indonesia Nomor 3 Tahun 2026 tentang Penanggulangan Penyakit (Berita Negara Republik Indonesia Tahun 2026 Nomor 173). Biro Hukum Kementerian Kesehatan Republik Indonesia. https://peraturan.go.id/files/permenkes-no-3-tahun-2026.pdf
Khanal, P., et al. (2023). Estimation of 10-year cardiovascular risk among adult population in western Nepal using nonlaboratory-based WHO/ISH chart, 2023: A cross-sectional study. Health Science Reports, 6(10), Article e1614. https://doi.org/10.1002/hsr2.1614
Koo, H. L., DuPont, H. L., & Musher, D. M. (2007). Fulminant amoebic colitis following loperamide use. Journal of Travel Medicine, 14(1), 61-62. https://doi.org/10.1111/j.1708-8305.2006.00095.x
Largeau, B., Cracowski, J. L., Lengellé, C., Sautenet, B., & Jonville-Béra, A. P. (2021). Drug-induced peripheral oedema: An aetiology-based review. British Journal of Clinical Pharmacology, 87(8), 3043-3055. https://doi.org/10.1111/bcp.14752
Liang, L., Kung, J. Y., Mitchelmore, B., Cave, A., & Banh, H. L. (2022). Comparative peripheral edema for dihydropyridines calcium channel blockers treatment: A systematic review and network meta-analysis. The Journal of Clinical Hypertension, 24(5), 536-554. https://doi.org/10.1111/jch.14436
Makani, H., Bangalore, S., Romero, J., Htyte, N., Berrios, R. S., Makwana, H., & Messerli, F. H. (2011). Peripheral edema associated with calcium channel blockers: Incidence and withdrawal rate—a meta-analysis of randomized trials. Journal of Hypertension, 29(7), 1270-1280. https://doi.org/10.1097/HJH.0b013e3283472643
Moffatt, C. J., Franks, P. J., Doherty, D. C., Williams, A. F., Badger, C., Jeffs, E., Bosanquet, N., & Mortimer, P. S. (2003). Lymphoedema: An underestimated health problem. QJM: An International Journal of Medicine, 96(10), 731-738. https://doi.org/10.1093/qjmed/hcg126
Mohiuddin, A. K. (2023). Erroneous uses of NSAIDs in patients with COVID-19, dengue, and chikungunya. Universal Journal of Pharmacy and Pharmacology, 2(1), 1-2. https://doi.org/10.31586/ujpp.2023.551
Outlaw, F., Meek, J., MacDonald, L. W., & Leung, T. S. (2020). Smartphone screening for neonatal jaundice via ambient-subtracted scleral chromaticity. PLOS One, 15(3), Article e0216970. https://pmc.ncbi.nlm.nih.gov/articles/PMC7051077/
Paz-Bailey, G., Adams, L. E., Deen, J., Anderson, K. B., & Katzelnick, L. C. (2024). Dengue. JAMA, 331(10), 874-884. https://doi.org/10.1001/jama.2023.27724
Pemerintah Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi (Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196). Sekretariat Negara Republik Indonesia.
Pemerintah Republik Indonesia. (2023). Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan (Lembaran Negara Republik Indonesia Tahun 2023 Nomor 105). Sekretariat Negara Republik Indonesia. https://gudangilmu.farmasetika.com/bab-ii-transformasi-teknologi-kesehatan-blueprint/
Perhimpunan Dokter Hipertensi Indonesia. (2019). Konsensus penatalaksanaan hipertensi di Indonesia (Tabel prediksi risiko PTM diadaptasi dari WHO Cardiovascular Disease Risk Charts). Perhimpunan Dokter Hipertensi Indonesia (InaSH). https://www.inash.or.id/
Perhimpunan Dokter Spesialis Kardiovaskular Indonesia & Perkumpulan Endokrinologi Indonesia. (2022). Panduan tata laksana dislipidemia di Indonesia. Pengurus Pusat PERKI & PB PERKENI.
Perhimpunan Dokter Spesialis Kardiovaskular Indonesia. (2025). Pedoman tatalaksana hipertensi pada penyakit kardiovaskular & sindrom koroner akut. Pengurus Pusat Perhimpunan Dokter Spesialis Kardiovaskular Indonesia (PERKI). https://www.inaheart.org/wp-content/uploads/2025/10/Pedoman-Tatalaksana-Hipertensi-Pada-Penyakit-Kardiovaskular.pdf
Perhimpunan Reumatologi Indonesia. (2024). Pedoman diagnosis dan tatalaksana hiperurisemia & artritis gout (Edisi pembaruan; ISBN: 978-979-3730-48-6). Pengurus Besar Perhimpunan Reumatologi Indonesia (IRA). https://reumatologi.or.id/wp-content/uploads/2024/09/ISBN-Hiperurisemia-Artritis-Gout_download.pdf
Perkumpulan Endokrinologi Indonesia. (2021). Pedoman petunjuk praktis terapi insulin pada pasien diabetes melitus tahun 2021. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://papdisolo.com/library
Perkumpulan Endokrinologi Indonesia. (2024). Pedoman pengelolaan dan pencegahan diabetes melitus tipe 2 dewasa di Indonesia tahun 2024. Pengurus Besar Perkumpulan Endokrinologi Indonesia (PERKENI). https://pbperkeni.or.id/wp-content/uploads/2025/08/DMT2-2024-Protected.pdf
Putri, R. A., et al. (2025). Pengaruh penggunaan amlodipine terhadap risiko edema perifer pada pasien hipertensi. Jurnal Sains dan Kesehatan, 7(3), 213-221. https://doi.org/10.25026/jsk.v7i3.2460
Rezaei, F., Seif, M., Fattahi, M. R., Gandomkar, A., & Hasanzadeh, J. (2023). Comparison of laboratory-based and non-laboratory-based WHO cardiovascular disease risk charts: A population-based study. The Lancet Diabetes & Endocrinology, 11(7), 480-490. https://doi.org/10.1016/S2213-8587(23)00119-5
Satrija, F., Ridwan, Y., Jastal, Samarang, & Rauf, A. (2017). Current status of schistosomiasis in Indonesia: Epidemiology, transmission, and integrated control. Infectious Diseases of Poverty, 6(1), 1-14. https://doi.org/10.1186/s40249-017-0256-8
Savage, R. D., Visentin, J. D., Bronskill, S. E., Wang, X., Gruneir, A., Giannakeas, V., Guan, J., Lam, K., Luke, M. J., Read, S. H., Stall, N. M., Wu, W., Zhu, L., Rochon, P. A., & McCarthy, L. M. (2020). Evaluation of a common prescribing cascade of calcium channel blockers and diuretics in older adults with hypertension. JAMA Internal Medicine, 180(5), 643-651. https://doi.org/10.1001/jamainternmed.2019.7087
Schiller, L. R., et al. (2020). Severe acute diarrhea: Pathophysiology, antimotility contraindications, and management (PMCID: PMC7127018). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC7127018/
Sharp, T. M., Keating, M. K., Shieh, W. J., Bhatnagar, J., Bollweg, B. C., Levine, R., Blau, D. M., Torres, J. V., Rivera, A., Perez-Padilla, J., Munoz-Jordan, J., Sanabria, D., Fischer, M., & Zaki, S. R. (2021). Clinical characteristics, histopathology, and tissue immunolocalization of chikungunya and dengue virus infections. Clinical Infectious Diseases, 73(2), e345-e354. https://doi.org/10.1093/cid/ciaa837
Sica, D. A. (2003). Calcium channel blocker-related peripheral edema: Can it be resolved? The Journal of Clinical Hypertension, 5(4), 291-295. https://doi.org/10.1111/j.1524-6175.2003.02402.x
Tovar, J. H., Pinzón, M. A., Rincón, D. F., et al. (2024). Anesthesia and perioperative care management in patients with dengue fever: Coagulopathy, plasma leakage, and comorbid medications. Brazilian Journal of Anesthesiology, 74(4), Article 844521. https://pmc.ncbi.nlm.nih.gov/articles/PMC11233874/
U.S. Centers for Disease Control and Prevention. (2024). CDC clinical guidance for dengue & contraindication of NSAIDs. U.S. Department of Health and Human Services.
U.S. National Library of Medicine, National Institutes of Health. (2024a). Angiotensin-converting enzyme inhibitors (ACEI) (StatPearls Bookshelf ID: NBK431051). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK431051/
U.S. National Library of Medicine, National Institutes of Health. (2024b). DailyMed official drug monograph: Loperamide hydrochloride capsule (SetID: 1be585e2-ef49-4210-8a2d-22a326e4cc1b). National Institutes of Health. https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1be585e2-ef49-4210-8a2d-22a326e4cc1b
U.S. National Library of Medicine, National Institutes of Health. (2024c). Ibuprofen (StatPearls Bookshelf ID: NBK542299). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK542299/
U.S. National Library of Medicine, National Institutes of Health. (2024d). Loperamide (StatPearls Bookshelf ID: NBK557885). StatPearls Publishing. https://www.ncbi.nlm.nih.gov/sites/books/NBK557885/
Wang, L., et al. (2021). Neonatal jaundice detection using a computer vision system. Designs, 5(4), Article 63. https://doi.org/10.3390/designs5040063
Wang, Y., et al. (2023). Non-invasive and non-contact automatic jaundice detection of neonates and adults using computer vision. Computer Methods in Biomechanics and Biomedical Engineering: Imaging & Visualization, 11(6), Article 2244601. https://doi.org/10.1080/21681163.2023.2244601
Widjaja, J., Anastasia, H., Nurwidayati, A., Nurjana, M. A., Mujiyanto, & Maksud, M. (2017). Situasi terkini daerah fokus keong hospes perantara di daerah endemis schistosomiasis di Sulawesi Tengah. Buletin Penelitian Kesehatan, 45(4), 215-222. https://doi.org/10.22435/bpk.v45i4.7570.215-222
World Health Organization. (2005). The treatment of diarrhoea: A manual for physicians and other senior health workers (4th rev., beserta Pedoman Lintas Diare Kemenkes RI). World Health Organization.
World Health Organization. (2009). Dengue: Guidelines for diagnosis, treatment, prevention and control (New ed.). World Health Organization. https://www.who.int/publications/i/item/9789241547871
World Health Organization, Regional Office for South-East Asia. (2011). Comprehensive guidelines for prevention and control of dengue and dengue haemorrhagic fever (Revised and expanded ed.). World Health Organization. https://iris.who.int/handle/10665/204894
World Health Organization. (2016). Updated guideline: Paediatric emergency triage, assessment and treatment (ETAT) (beserta Buku Bagan MTBS Kemenkes RI). World Health Organization.
World Health Organization. (2018). WHO expert consultation on rabies: Third report (beserta Petunjuk Teknis Penatalaksanaan Kasus GHPR Kemenkes RI). World Health Organization.
World Health Organization. (2022). Ending the neglect to attain the Sustainable Development Goals: A strategic framework for integrated control and management of skin-related neglected tropical diseases. World Health Organization. https://www.who.int/publications/i/item/9789240051423
World Health Organization. (2023). WHO guidelines for malaria (beserta PNPK Tata Laksana Malaria Kemenkes RI). World Health Organization.
World Health Organization Indonesia. (2023, July 25). Overcoming challenges to eliminate schistosomiasis in Central Sulawesi (Mengatasi tantangan untuk mengeliminasi schistosomiasis di Sulawesi Tengah). World Health Organization. https://www.who.int/indonesia/id/news/detail/25-07-2023-overcoming-challenges-to-eliminate-schistosomiasis-in-central-sulawesi
Yotsu, R. R., Ding, Z., Hamm, J., & Blanton, R. E. (2023a). Deep learning for AI-based diagnosis of skin-related neglected tropical diseases: A pilot study. PLOS Neglected Tropical Diseases, 17(8), Article e0011230. https://doi.org/10.1371/journal.pntd.0011230
Yotsu, R. R., et al. (2023b). Integrated control and management of skin-related neglected tropical diseases. PLOS Neglected Tropical Diseases, 17(6), Article e0011357. https://doi.org/10.1371/journal.pntd.0011357
Yotsu, R. R., Oiwoh, S. O., Mbali, H., Parajuli, N., Enbiale, W., & Ruiz-Postigo, J. A. (2025). Harnessing artificial intelligence for skin-related neglected tropical diseases (skin NTDs): Opportunities, challenges and future directions. International Health, 17(5), 792-794. https://doi.org/10.1093/inthealth/ihaf068
Zhang, H., et al. (2024). Robust visual identification of under-resourced dermatological conditions: Background pixel separation on the Fitzpatrick 17k dataset in lower and middle income countries (PMCID: PMC12099365). National Center for Biotechnology Information. https://pmc.ncbi.nlm.nih.gov/articles/PMC12099365/
Zheng, X., et al. (2026). Incidence and risk factors of calcium channel blocker-related edema in hypertensive patients: A multicenter retrospective cohort study. PLOS One, 21(3), Article e0336659. https://doi.org/10.1371/journal.pone.0336659

