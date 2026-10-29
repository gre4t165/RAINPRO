from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from rainpro.__main__ import main
from rainpro.config import AudioConfig, load_config
from rainpro.engine import BlockSource, SilenceSource


class ConfigTests(unittest.TestCase):
    def load_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.toml'
            path.write_text(text, encoding='utf-8')
            return load_config(path)

    def test_example_matches_defaults(self):
        path = Path(__file__).resolve().parents[1] / 'config/default.toml'
        self.assertEqual(load_config(path), AudioConfig())
        self.assertEqual(load_config(), AudioConfig())

    def test_partial_override(self):
        self.assertEqual(self.load_text('[audio]\nsample_rate = 44100').sample_rate, 44100)

    def test_invalid_configuration_is_rejected(self):
        for text in ('[audio]\nchannels=1', '[audio]\nblock_frames=0',
                     '[audio]\nblock_frames=8193', '[audio]\nsample_rate=32000',
                     '[audio]\nchannels=true', '[audio]\nchannels=2.0',
                     '[audio]\nblock_frames="1024"', '[audio]\nchanels=2',
                     '[unknown]\nx=1', 'audio=1', '[broken'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.load_text(text)

    def test_cli_reports_missing_or_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'missing.toml'
            error = StringIO()
            with redirect_stderr(error):
                self.assertEqual(main(['--check', '--config', str(path)]), 2)
            self.assertIn('Configuration error', error.getvalue())
            path.write_text('[audio]\nchannels=1', encoding='utf-8')
            with redirect_stderr(StringIO()):
                self.assertEqual(main(['--check', '--config', str(path)]), 2)

    def test_headless_path_does_not_load_qt(self):
        script = ('import sys; from rainpro.__main__ import main; '
                  'assert main(["--check"]) == 0; '
                  'assert not any(m.startswith("PySide6") for m in sys.modules)')
        result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


class AudioContractTests(unittest.TestCase):
    def test_bounded_blocks_are_filled_in_place(self):
        config = AudioConfig()
        source: BlockSource = SilenceSource(config)
        block = np.empty((config.block_frames, config.channels), dtype=np.float32)
        address = block.ctypes.data
        for frames in (config.block_frames, 1, 127, config.block_frames):
            view = block[:frames]
            view.fill(np.nan)
            source.render_into(view)
            self.assertEqual(view.ctypes.data, address)
            self.assertEqual(view.shape, (frames, 2))
            self.assertTrue(np.isfinite(view).all())
            self.assertTrue((view == 0).all())

    def test_invalid_buffers_are_rejected(self):
        readonly = np.zeros((64, 2), dtype=np.float32)
        readonly.flags.writeable = False
        buffers = [None, np.zeros((64, 2)), np.zeros(128, dtype=np.float32),
                   np.zeros((0, 2), dtype=np.float32),
                   np.zeros((1025, 2), dtype=np.float32),
                   np.zeros((64, 1), dtype=np.float32),
                   np.zeros((64, 4), dtype=np.float32)[:, ::2], readonly]
        source = SilenceSource(AudioConfig())
        for output in buffers:
            with self.subTest(shape=getattr(output, 'shape', None)):
                with self.assertRaises(ValueError):
                    source.render_into(output)

    def test_engine_does_not_import_ui_or_devices(self):
        script = ('import sys; import rainpro.engine; '
                  'assert not any(m.startswith(("PySide6", "rainpro.ui", "sounddevice")) '
                  'for m in sys.modules)')
        result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
