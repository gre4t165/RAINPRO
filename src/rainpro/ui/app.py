"""Minimal desktop shell. Audio processing must not run on the UI thread."""
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

from rainpro.config import AudioConfig


def create_window(config: AudioConfig) -> QMainWindow:
    window = QMainWindow()
    window.setWindowTitle("Rain ASMR Studio — Foundation")
    window.resize(760, 420)
    body = QWidget()
    layout = QVBoxLayout(body)
    layout.setContentsMargins(32, 32, 32, 32)
    title = QLabel("Rain ASMR Studio")
    title.setStyleSheet("font-size: 26px; font-weight: 600")
    layout.addWidget(title)
    layout.addWidget(QLabel("Fondasi desktop · tahap 1"))
    layout.addWidget(QLabel(
        f"{config.sample_rate:,} Hz · stereo · {config.block_frames} frames/blok"
    ))
    note = QLabel("Konfigurasi siap. Sintesis dan pemutaran audio belum diimplementasikan.")
    note.setWordWrap(True)
    layout.addWidget(note)
    layout.addStretch()
    window.setCentralWidget(body)
    window.statusBar().showMessage("Engine terpisah dari UI")
    return window


def run(config: AudioConfig) -> int:
    app = QApplication([])
    app.setApplicationName("Rain ASMR Studio")
    window = create_window(config)
    window.show()
    return app.exec()
