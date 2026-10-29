"""Bounded block interface. Silence is a diagnostic source, not rain synthesis."""
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from rainpro.config import AudioConfig


class BlockSource(Protocol):
    def render_into(self, output: NDArray[np.float32]) -> None:
        """Fill caller-owned C-contiguous float32 (frames, channels) PCM.

        Values must be finite and within [-1, 1]. A call may render between
        1 and config.block_frames frames. Ownership stays with the caller.
        Future stateful implementations must preserve state between calls.
        """
        ...


class SilenceSource:
    def __init__(self, config: AudioConfig) -> None:
        self._config = config

    def render_into(self, output: NDArray[np.float32]) -> None:
        if not isinstance(output, np.ndarray):
            raise ValueError("output must be a NumPy array")
        if output.dtype != np.float32 or output.ndim != 2:
            raise ValueError("output must be float32 with shape (frames, channels)")
        frames, channels = output.shape
        if not 1 <= frames <= self._config.block_frames:
            raise ValueError("output frame count is outside the configured block limit")
        if channels != self._config.channels:
            raise ValueError("output channel count does not match configuration")
        if not output.flags.c_contiguous or not output.flags.writeable:
            raise ValueError("output must be writable and C-contiguous")
        output.fill(0.0)
