"""Immutable configuration shared by the engine and application."""
from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True, slots=True)
class AudioConfig:
    sample_rate: int = 48000
    channels: int = 2
    block_frames: int = 1024

    def __post_init__(self) -> None:
        for name in ("sample_rate", "channels", "block_frames"):
            if type(getattr(self, name)) is not int:
                raise ValueError(f"{name} must be an integer")
        if self.sample_rate not in (44100, 48000):
            raise ValueError("sample_rate must be 44100 or 48000")
        if self.channels != 2:
            raise ValueError("channels must be 2 (stereo)")
        if not 64 <= self.block_frames <= 8192:
            raise ValueError("block_frames must be between 64 and 8192")


def load_config(path: Path | None = None) -> AudioConfig:
    if path is None:
        return AudioConfig()
    with path.open("rb") as stream:
        data = tomllib.load(stream)
    if set(data) - {"audio"}:
        raise ValueError("Only the [audio] configuration section is supported")
    audio = data.get("audio", {})
    if not isinstance(audio, dict):
        raise ValueError("audio must be a TOML table")
    if set(audio) - {"sample_rate", "channels", "block_frames"}:
        raise ValueError("Unknown audio configuration key")
    return AudioConfig(**audio)
