# Keputusan fondasi

## Keadaan yang ditinjau, 29 Oktober 2026

`gre4t165/RAINPRO` kosong: contents mengembalikan “This repository is empty”, daftar branch/issue/PR kosong. Tidak ada AGENTS.md atau implementasi GitHub untuk dilanjutkan saat pemeriksaan.

Kedua arsip sebelumnya diperiksa: `Rain_ASMR_Studio.zip` dan `Rain_ASMR_Studio_Source.zip` sudah memakai Python, PySide6 dan NumPy, tetapi main.py menggabungkan UI, antrean, preview dan scheduler. Versi source juga membawa bytecode __pycache__. Arsip adalah prototipe referensi, bukan baseline yang sudah tervalidasi. Fondasi ini mempertahankan arah stack dan pemisahan engine/UI; kode DSP, preset dan fitur ekspor tidak disalin sebelum audit dan uji mendengar. Tidak ada klaim bahwa fitur arsip telah dipindahkan.

## Arah dependency

`__main__ → config + ui`; `ui → config`; `engine → config + NumPy`.
Engine tidak mengimpor Qt atau mengakses perangkat audio. Entry point mengimpor UI hanya saat menjalankan desktop. Paket core dapat dipasang dan diuji tanpa PySide6.

Dependency desktop hanya PySide6-Essentials (QtCore/QtGui/QtWidgets), tanpa paket Addons/WebEngine. Python 3.12 menjadi baseline; PySide6 mempertahankan arah prototipe dan menyediakan UI desktop Qt Widgets. NumPy menjadi representasi PCM sekaligus dasar operasi DSP vectorized. Tidak perlu SciPy, FFmpeg, sounddevice, database atau AI model pada tahap ini. Dokumentasi resmi Qt: https://doc.qt.io/qtforpython-6/gettingstarted.html

## Kontrak PCM

- PCM float32, C-contiguous, `(frames, 2)`, urutan kanal kiri/kanan; 44.1/48 kHz, default 48 kHz.
- Caller memiliki buffer; sumber mengisi buffer yang sudah dialokasikan. Maksimum `block_frames` per panggilan; blok akhir boleh lebih pendek.
- Sampel harus finite dalam [-1, 1]. SilenceSource hanya menghasilkan nol untuk menguji sambungan kontrak; belum ada DSP atau perangkat output.
- Memori kerja harus proporsional terhadap ukuran blok, bukan durasi proyek. Hindari alokasi sepanjang berjam-jam.
- Implementasi sumber stateful kelak harus mempertahankan state/RNG dan kontinuitas antarblok. Thread yang memiliki sumber bertanggung jawab atas akses; kontrak belum menjamin thread safety atau hard real time.

## Batas UI dan pekerjaan berat

Shell hanya menampilkan konfigurasi. Saat preview/render ditambahkan, controller/worker akan memiliki sumber dan lifecycle cancellation; UI mengirim snapshot konfigurasi immutable dan menerima progress/error melalui signal. Jangan melakukan sintesis, I/O atau encoding dalam slot UI. Jangan membuat thread, antrean atau abstraksi backend kosong sebelum jalur audio pertama memerlukannya.

Windows 11 adalah target rilis pertama. Tes Linux membantu portabilitas, bukan bukti dukungan perangkat Windows. Belum ada executable/installer. Tinjau lisensi dependency Qt dan siapkan notice sebelum distribusi; lisensi proyek belum ditentukan pemilik.
