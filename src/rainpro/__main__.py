"""Composition root. Headless checks do not import the optional UI."""
import argparse
from pathlib import Path
import sys

from rainpro.config import load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rain ASMR Studio foundation")
    parser.add_argument("--config", type=Path, help="Optional TOML configuration")
    parser.add_argument("--check", action="store_true", help="Validate configuration without UI")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    if args.check:
        print(f"Configuration OK: {config.sample_rate} Hz, {config.channels} channels, "
              f"{config.block_frames} frames/block")
        return 0
    try:
        from rainpro.ui.app import run
    except ModuleNotFoundError as exc:
        if exc.name != "PySide6":
            raise
        print('Desktop dependency missing. Install: python -m pip install -e ".[desktop]"',
              file=sys.stderr)
        return 2
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
