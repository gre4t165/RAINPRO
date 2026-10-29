# RAINPRO — Rain ASMR Studio

Fondasi aplikasi desktop audio hujan untuk Windows 11, **Python 3.12 + PySide6/Qt Widgets**, tanpa Electron. Tahap ini menyediakan konfigurasi, kontrak blok audio yang bisa diuji tanpa UI, dan jendela native minimal. Belum menghasilkan atau memutar suara hujan.

## Mulai di Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -e ".[desktop]"
.venv\Scripts\python -m rainpro --check --config config/default.toml
.venv\Scripts\python -m rainpro
```

Untuk pengembangan engine tanpa Qt: `python -m pip install -e .`.
Jalankan pengujian: `python -m unittest discover -s tests -v`.
Linux/macOS: gunakan `.venv/bin/python` sebagai pengganti `.venv\Scripts\python`.
Konfigurasi bawaan bekerja dari direktori mana pun; `--config` hanya diperlukan untuk override TOML.

## Struktur

- `src/rainpro/engine/`: kontrak PCM dan sumber silence untuk diagnostik.
- `src/rainpro/ui/`: shell Qt; dependency desktop bersifat opsional.
- `src/rainpro/config.py`: konfigurasi immutable dan validasi TOML.
- `src/rainpro/__main__.py`: entry point/composition root.
- `config/`, `tests/`, `docs/`: contoh konfigurasi, tes, keputusan dan milestone.

[Arsitektur](docs/architecture.md) · [Milestone](docs/milestones.md).
Rentang dependency di pyproject belum merupakan lockfile; bekukan dependency rilis setelah validasi Windows. CI memeriksa Python 3.12/3.13 di Windows dan Linux, termasuk smoke test Qt tanpa perangkat audio.
