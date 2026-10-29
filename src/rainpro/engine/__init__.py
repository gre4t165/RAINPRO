"""Headless audio contracts; no UI, device, filesystem or Qt dependencies."""
from .source import BlockSource, SilenceSource

__all__ = ["BlockSource", "SilenceSource"]
