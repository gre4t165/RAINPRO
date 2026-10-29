"""Requires desktop extra; CI runs with QT_QPA_PLATFORM=offscreen."""
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from rainpro.config import AudioConfig
from rainpro.ui.app import create_window

app = QApplication([])
window = create_window(AudioConfig())
window.show()
app.processEvents()
assert window.isVisible()
assert window.windowTitle().startswith('Rain ASMR Studio')
QTimer.singleShot(50, window.close)
QTimer.singleShot(5000, lambda: app.exit(1))
assert app.exec() == 0
assert not window.isVisible()
print('Qt window open/close OK')
