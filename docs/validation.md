# Validasi scaffold — 29 Oktober 2026

Dijalankan lokal di Linux dengan Python 3.12.14, NumPy 2.3.5 dan Qt/PySide6 6.12.0:

- Build editable/entry point berhasil.
- `python -m unittest discover -s tests -v`: 8 tes lulus, termasuk validasi konfigurasi, buffer invalid, isi buffer in-place dan isolasi dependency engine/UI.
- `python -m rainpro --check --config config/default.toml`: berhasil.
- `QT_QPA_PLATFORM=offscreen python tests/smoke_ui.py`: jendela berhasil dibuka dan ditutup otomatis. Ini bukan pemeriksaan visual desktop interaktif.
- Kompilasi sintaks seluruh source dan tests: berhasil.

Desktop dependency akhir menggunakan PySide6-Essentials. Tidak ada import Addons/WebEngine. CI disediakan untuk Python 3.12/3.13 pada Windows dan Linux; hasil remote harus dilihat terpisah. Uji perangkat audio, kualitas hujan, installer dan desktop Windows interaktif belum dilakukan karena belum termasuk implementasi tahap ini.
