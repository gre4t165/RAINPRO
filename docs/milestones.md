# Urutan milestone

Setiap tahap dimulai setelah kriteria tahap sebelumnya terpenuhi. Estimasi adalah hari kerja pengembangan, bukan komitmen tanggal.

| Tahap | Cakupan minimal | Kriteria selesai | Estimasi |
| --- | --- | --- | --- |
| 1 — Fondasi | Packaging, konfigurasi, kontrak blok, shell Qt, tes dan CI | Instalasi bersih, headless check, tes dan buka/tutup jendela berhasil di Windows 11 | 1–2 hari |
| 2 — Satu engine hujan | Satu sumber seeded/stateful, satu parameter intensitas; benchmark per blok | Reproducible untuk seed dan parameter sama, finite, tanpa clipping/klik batas blok; memori stabil untuk stream panjang; evaluasi mendengar | 2–4 hari |
| 3 — Preview perangkat | Satu output device, play/stop, worker/controller, error perangkat dan cancellation | UI responsif, start/stop berulang aman, shutdown bersih, underrun terukur pada PC Windows target | 2–3 hari |
| 4 — Render offline WAV | Streaming PCM16 dengan progress/cancel dan penanganan file sementara | Durasi/frame/header tepat, memori stabil, pembatalan bersih; batas RIFF 4 GiB ditolak/ditangani eksplisit | 2–3 hari |
| 5 — Distribusi dasar | Dependency terkunci, paket Windows, notice lisensi, petunjuk pengguna | Instalasi dan buka/preview/render di Windows bersih tanpa Python pengembang | 2–3 hari |

Tahap 1 di repository adalah scaffold; hasil CI dan smoke test Windows tetap harus diperiksa sebelum menyatakan milestone Windows selesai. Kualitas suara dinilai ketika tahap 2 tersedia, bukan dari kelulusan tes silence.

Setelah lima tahap stabil: mixer multilayer/preset → FLAC/MP3 → antrean batch persisten → scheduler dan pemulihan job. Setiap fitur membutuhkan acceptance test tersendiri. Scheduler mandiri saat UI ditutup memerlukan keputusan lifecycle proses/Windows Task Scheduler, bukan sekadar QTimer. Integrasi model elephant-goldfish ditunda sampai kegunaannya untuk audio, kebutuhan runtime, lisensi dan performa sudah diperiksa; bukan dependency fondasi.
