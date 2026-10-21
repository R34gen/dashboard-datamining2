# Dashboard Pendidikan Jawa Timur — GitHub Pages & Streamlit Cloud

Dashboard interaktif yang diekstrak dari **`Pratinjau_Visual_Dashboard_Jatim (2).html`** milik pengguna. Paket ini dapat dipasang ke **GitHub Pages** sebagai website statis tanpa Python, atau tetap menggunakan alamat **Streamlit Community Cloud** dengan `app.py` baru yang menampilkan dashboard HTML yang sama. Data dan visualisasi sumber tetap berasal dari file HTML yang diunggah.

## Fitur

- Ringkasan IPM dan peringkat kabupaten/kota
- Peta interaktif dengan penanda, klaster, dan pewarnaan IPM
- Perbandingan IPM dan rata-rata lama sekolah
- Rasio murid per guru dan murid per sekolah
- Komposisi sekolah, guru, dan murid SD/SMP/SMA
- Perbandingan dua kabupaten/kota
- Tabel data dan unduh CSV sesuai filter
- Filter jenis wilayah, pemilihan kabupaten/kota, dan rentang IPM

**Cakupan data:** 38 wilayah (29 kabupaten dan 9 kota), tahun integrasi 2025, sesuai isi file HTML yang diberikan.

## Cara mengunggah ke GitHub

1. Ekstrak paket ZIP ini.
2. Buat repositori GitHub baru (mis. `dashboard-pendidikan-jatim`).
3. Unggah **seluruh isi folder ini**, terutama `index.html` dan folder `assets/`, `data/`, `maps/`, agar struktur direktori tetap sama.
4. Di GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → `main` → `/ (root)` → Save**.
5. Setelah deployment berhasil, buka alamat `https://USERNAME.github.io/NAMA_REPO/`.

### Mengatasi `ModuleNotFoundError: No module named peta` di Streamlit Cloud

Repositori Anda sebelumnya masih menggunakan `app.py` lama yang mengimpor modul `peta.py` dan `visualisasi.py`, padahal kedua modul tersebut tidak termasuk dalam paket HTML. **Ganti `app.py` lama dengan `app.py` dari paket ini**. File baru tidak mengimpor `peta`/`visualisasi`, melainkan menggabungkan `index.html` dan semua aset JS/CSS menjadi satu halaman agar dapat dimuat di Streamlit iframe. Pastikan `requirements.txt` baru juga ada di root, bersama `index.html` dan folder `assets`.

1. Buka repositori `dashboard-datmin` → **Add file → Upload files**.
2. Unggah `app.py` dan `requirements.txt` baru **menimpa versi lama**, beserta file dashboard lainnya yang belum ada. Jangan tempatkan berkas ke subfolder.
3. Commit ke branch `main`. Di Streamlit Cloud pilih **Reboot app** bila aplikasi tidak otomatis berjalan ulang.
4. Pertahankan **Main file path**: `app.py`. `peta.py` dan `visualisasi.py` tidak lagi dibutuhkan oleh aplikasi ini.

> Jika layar dashboard terlalu panjang atau pendek, ubah `height=1550` pada baris terakhir `app.py`. Dashboard dapat discroll di dalam iframe.

### Cara menjalankan

Buka `index.html` dengan browser (double-click) atau melalui GitHub Pages. Untuk menjalankannya melalui Streamlit, gunakan `streamlit run app.py`. Seluruh pustaka yang dibutuhkan telah disalin secara lokal; browser tidak perlu memuat CDN. Untuk localhost opsional: `python -m http.server 8000` lalu `http://localhost:8000/`.

## Struktur berkas

```
index.html
app.py                       # Entry point Streamlit Cloud (tanpa peta.py)
requirements.txt             # Dependensi Streamlit
assets/
  css/style.css              # Gaya antarmuka
  js/app.js                  # Logika dashboard, filter, grafik, perbandingan
  js/analytics.js            # Fungsi analisis dan ekspor CSV
  js/dataset.js              # Salinan siap pakai dari JSON data
  js/coordinates.js          # Salinan siap pakai dari JSON koordinat
  js/map-template.js         # Bundel peta lengkap untuk kompatibilitas offline
  js/vendor/plotly.min.js    # Plotly.js tersimpan lokal
maps/map-template.html        # Template peta Leaflet dan geometri (sumber dapat diedit)
data/jatim-2025.json         # Snapshot indikator 38 wilayah
data/koordinat-wilayah.json # Koordinat tiap kabupaten/kota
data/jatim-2025.csv         # Data dalam format CSV
scripts/sinkronkan_data.py    # Pembaruan file JS dan CSV setelah sumber diedit
tests/test-data.js            # Validasi struktur dataset
THIRD_PARTY_NOTICES.md        # Atribusi pustaka
```

## Memperbarui data

1. Edit `data/jatim-2025.json` (dan koordinat bila berubah).
2. Jalankan `python scripts/sinkronkan_data.py`.
3. Upload/commit semua berkas yang diperbarui.

Data JSON/CSV disediakan untuk transparansi dan analisis lebih lanjut. Browser menggunakan salinan `assets/js/dataset.js` supaya dashboard juga dapat dibuka langsung dari disk (tanpa masalah CORS `file://`). **Setelah mengubah JSON, wajib menjalankan sinkronisasi.**

## Batasan dan asal data

- **Ini rekonstruksi dari satu file pratinjau HTML**, bukan pemulihan keseluruhan proyek Streamlit, database SQLite, atau seluruh source repositori lama. `app.py` baru adalah wadah untuk menjalankan rekonstruksi HTML tersebut di Streamlit, bukan reproduksi kode Python asli.
- Data, geometri peta, serta fungsi diperoleh dari HTML tersebut; tidak ada angka yang diambil atau direka ulang dari internet.
- Snapshot mengandung data tahun integrasi 2025. **Sumber primer dan tahun asli data sekolah/guru/murid perlu diverifikasi** sebelum dipakai untuk publikasi akademik.
- Rata-rata IPM wilayah adalah rata-rata sederhana antardaerah, **bukan IPM resmi tingkat provinsi**.
- Rata-rata lama sekolah pada lampiran disebut untuk penduduk **15 tahun ke atas**, berbeda dari komponen RLS metode baru IPM (25 tahun ke atas); jangan menganggapnya ekuivalen.
- Peta dan pustakanya disematkan lokal, sehingga tidak membutuhkan tile online. Peta bersifat visualisasi agregat wilayah.

## Pengujian

Untuk memeriksa struktur data: `node tests/test-data.js` (Node.js opsional). Antarmuka dan peta sebaiknya dicek di browser setelah penerapan.

## Atribusi

Paket ini memuat Plotly.js, Leaflet, Leaflet.markercluster, dan materi geospasial bawaan file sumber. Lihat `THIRD_PARTY_NOTICES.md` serta komentar lisensi di berkas vendor.
